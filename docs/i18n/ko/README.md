> [English](../../../README.md)

# somethingwithproof.github.io

https://somethingwithproof.github.io 소스입니다: 생성된 문서 페이지가 포함된 공개 리포지토리의 정적 갤러리입니다.

## 빌드

서드파티 Python 의존성 없이 Python 3.12와 GitHub CLI(`gh`)가 필요합니다:

```sh
python3 build.py --fetch   # refresh cache/ from GitHub, then build _site/
python3 build.py           # build from cache/
python3 -m http.server -d _site 8765
```

`content/sitemap.json`은 섹션, 주제 및 리포지토리를 정의합니다. 직접 작성한 페이지는 `content/pages/`에 있습니다. 프로젝트 페이지는 허용 목록 기반 HTML 새니타이저를 거친 리포지토리 README에서 생성됩니다. 나열된 리포지토리 중 비공개 리포지토리가 있거나 생성된 색상 대비율이 4.5:1 미만으로 떨어지면 빌드가 실패합니다.

## 현지화

UI 크롬, 탐색, 검색 및 레이블은 `locales/` 아래 45개 로캘(Tier 1 20개, 아프리카 15개, 아시아 10개)로 제공됩니다.

- 정적 HTML의 기본 언어는 영어이며 `python3 build.py --lang <locale>`을 통해 모든 로캘로 빌드할 수 있습니다.
- 헤더에는 브라우저 언어 자동 감지 기능과 RTL 로캘(`ar`, `ar-EG`, `ar-MA`, `fa`, `he`, `ur`)에 대한 `dir="rtl"` 지원을 갖춘 `/assets/locales/*.json` 기반 언어 전환기가 제공됩니다.
- `python3 -m unittest discover -s tests`로 로컬에서 검증합니다.

## 배포 및 라이선스

`.github/workflows/pages.yml`은 `main`에 푸시할 때마다 그리고 매일 GitHub Pages에 빌드 및 배포합니다. 전체 [영문 README](../../../README.md)와 [LICENSE](../../../LICENSE)를 참조하세요.
