#!/usr/bin/env python3
"""제품별이미지/ 의 사진을 index.html 제품 슬롯에 내장(embed)한다.

index.html 은 브라우저에서 asset 을 풀어 렌더링하는 번들 페이지이며, 내부의
DC 런타임은 HTML/CSS 의 URL(예: img src, style url())을 모두 제거(sanitize)한다.
그래서 이미지는 렌더링이 끝난 뒤 런타임 스크립트가 DOM API 로 직접 칠한다.
(DOM 으로 준 style 은 sanitizer 대상이 아니므로 살아남는다.)

이 스크립트는 몇 번을 실행해도 같은 결과가 되도록(idempotent) 작성되었다:
  1) 아직 <image-slot> 이 남아 있으면 data-img 훅을 가진 <div> 로 교체
  2) 주입 스크립트가 없으면 body 끝에 추가
  3) 주입 스크립트의 이미지 맵(var M={...})을 항상 최신 이미지로 재생성
"""
import base64, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(ROOT, "제품별이미지")
HTML = os.path.join(ROOT, "index.html")

# 제품 슬롯 id -> 이미지 파일명
MAPPING = {
    "prod1": "컴배트 스피드 에어졸.jpg",
    "prod2": "컴배트 파워형 베이트.jpg",
    "prod3": "컴배트 스피드 에어졸 (개미용).jpg",
    "prod4": "컴배트 파워형 베이트 (개미용).jpg",
}


def datauri(fn):
    with open(os.path.join(IMG_DIR, fn), "rb") as f:
        # url() 을 따옴표 없이 쓰므로 base64(공백/따옴표/괄호 없음)만 넣는다
        return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode("ascii")


def build_entries():
    return ",".join("%s:'%s'" % (sid, datauri(fn)) for sid, fn in MAPPING.items())


def make_script(entries):
    return (
        "\\n<script>\\n"
        "(function(){var M={" + entries + "};"
        "function a(){document.querySelectorAll('[data-img]').forEach(function(x){"
        "var u=M[x.getAttribute('data-img')];"
        "if(u){x.style.backgroundImage='url('+u+')';x.style.backgroundSize='contain';"
        "x.style.backgroundPosition='center';x.style.backgroundRepeat='no-repeat';}});}"
        "a();new MutationObserver(a).observe(document.documentElement,{childList:true,subtree:true});"
        "})();\\n<\\u002Fscript>\\n"
    )


def main():
    with open(HTML, "r", encoding="utf-8") as f:
        content = f.read()

    # 1) <image-slot> -> <div data-img=...> (최초 1회 마이그레이션)
    old_slot = ('<image-slot id=\\"{{ p.sid }}\\" shape=\\"rounded\\" radius=\\"14\\" '
                'placeholder=\\"제품 사진\\" fit=\\"contain\\" style=\\"width:100%;height:100%;\\">'
                '<\\u002Fimage-slot>')
    new_slot = ('<div role=\\"img\\" aria-label=\\"{{ p.name }}\\" data-img=\\"{{ p.sid }}\\" '
                'style=\\"width:100%;height:100%;\\"><\\u002Fdiv>')
    if old_slot in content:
        content = content.replace(old_slot, new_slot)
        print("image-slot -> div 교체 완료")

    entries = build_entries()
    script = make_script(entries)

    # 3) 기존 주입 스크립트의 M 맵만 갱신, 없으면 2) 새로 주입
    if "querySelectorAll('[data-img]')" in content:
        content = re.sub(r"var M=\{[^}]*\}", "var M={" + entries + "}", content, count=1)
        print("이미지 맵 갱신 완료")
    else:
        marker = '<\\u002Fbody><\\u002Fhtml>'
        if marker not in content:
            print("body 종료 마커를 찾지 못했습니다", file=sys.stderr)
            return 1
        content = content.replace(marker, script + marker, 1)
        print("이미지 주입 스크립트 추가 완료")

    with open(HTML, "w", encoding="utf-8") as f:
        f.write(content)

    for sid, fn in MAPPING.items():
        print("  %s <- %s" % (sid, fn))
    print("완료")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
