#!/usr/bin/env python3
"""제품 사진을 index.html에 data URI로 내장해 단일 파일로 만든다."""

import base64
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "index.html"
IMG_DIR = ROOT / "제품별이미지"
IMAGES = ("활명수 유.jpg", "꼬마활명수.jpg")


def main():
    content = HTML.read_text(encoding="utf-8")
    changed = 0

    for filename in IMAGES:
        source = f"제품별이미지/{filename.replace(' ', '%20')}"
        if source not in content:
            continue
        encoded = base64.b64encode((IMG_DIR / filename).read_bytes()).decode("ascii")
        content = content.replace(source, f"data:image/jpeg;base64,{encoded}")
        changed += 1

    if not changed:
        print("내장할 외부 이미지가 없습니다.")
        return 0

    HTML.write_text(content, encoding="utf-8")
    print(f"제품 이미지 {changed}개를 index.html에 내장했습니다.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
