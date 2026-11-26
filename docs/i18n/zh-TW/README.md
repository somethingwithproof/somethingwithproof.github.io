> [English](../../../README.md)

# somethingwithproof.github.io

https://somethingwithproof.github.io 的原始碼：一個包含自動產生文件頁面的公開儲存庫靜態藝廊。

## 建置

需要 Python 3.12 與 GitHub CLI（`gh`），無須任何第三方 Python 相依套件：

```sh
python3 build.py --fetch   # refresh cache/ from GitHub, then build _site/
python3 build.py           # build from cache/
python3 -m http.server -d _site 8765
```

`content/sitemap.json` 定義區段、主題與儲存庫。手寫頁面位於 `content/pages/`。專案頁面則是將各儲存庫的 README 透過允許清單 HTML 淨化器（sanitizer）處理後產生。若任何列出的儲存庫為私有，或任何產生的色彩對比度低於 4.5:1，建置將會失敗。

## 在地化

UI 外觀介面、導覽列、搜尋與標籤皆以 45 種語系隨附於 `locales/` 下（20 種 Tier 1 語系、15 種非洲語系與 10 種亞洲語系）。

- 靜態 HTML 預設為英文，並可透過 `python3 build.py --lang <locale>` 建置為任何語系。
- 頁首提供由 `/assets/locales/*.json` 支援的語言切換器，具備瀏覽器語言自動偵測功能，並為 RTL 語系（`ar`、`ar-EG`、`ar-MA`、`fa`、`he`、`ur`）提供 `dir="rtl"` 支援。
- 請使用 `python3 -m unittest discover -s tests` 在本機進行驗證。

## 部署與授權條款

`.github/workflows/pages.yml` 會在每次推送至 `main` 分支時以及每日自動建置並部署至 GitHub Pages。請參閱[英文 README](../../../README.md)與 [LICENSE](../../../LICENSE)。
