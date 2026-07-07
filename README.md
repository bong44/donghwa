# 동화제약 × 헨켈 컴배트 · 영업 자료

바퀴·개미 살충제(컴배트) 프로모션 가격 안내 페이지입니다.
구매 금액대별 사은품 안내와 4개 품목 가격표, 제품 이미지가 포함되어 있습니다.

- **진입점:** [`index.html`](index.html) — 외부 의존성 없는 단일 자체 완결(self-contained) 페이지
- **제품 이미지:** `index.html` 안에 data URI로 내장되어 있습니다. 원본은 [`제품별이미지/`](제품별이미지) 폴더 참고.

## GitHub Pages 배포 방법

### 1. 저장소에 올리기

```bash
git remote add origin https://github.com/<사용자명>/<저장소명>.git
git push -u origin main
```

### 2. Pages 활성화

GitHub 저장소 → **Settings → Pages → Build and deployment** 에서
**Source** 를 **GitHub Actions** 로 선택합니다.

이후 `main`(또는 `master`) 브랜치에 push 하면
[`.github/workflows/deploy.yml`](.github/workflows/deploy.yml) 워크플로가 자동으로 배포합니다.

배포가 끝나면 아래 주소에서 확인할 수 있습니다.

```
https://<사용자명>.github.io/<저장소명>/
```

> ⚠️ 이 페이지는 브라우저에서 asset을 풀어서 렌더링하므로 `file://` 로 직접 열면
> 동작하지 않습니다. GitHub Pages(HTTPS)처럼 웹 서버로 서빙해야 정상 표시됩니다.

## 제품 이미지 교체

`index.html` 하단에 각 제품 슬롯(`data-img="prod1"`~`prod4"`)에 이미지를 칠하는
스크립트가 있습니다. 이미지를 바꾸려면 `제품별이미지/` 의 파일을 교체한 뒤
`scripts/embed_images.py` 를 다시 실행하면 됩니다. (아래 스크립트는 참고용)
