> [English](../../../README.md)

# somethingwithproof.github.io

https://somethingwithproof.github.io 的源码仓库：一个展示公开仓库并自动生成文档页面的静态网站。

## 构建

需要 Python 3.12 和 GitHub CLI（`gh`），无需任何第三方 Python 依赖：

```sh
python3 build.py --fetch   # refresh cache/ from GitHub, then build _site/
python3 build.py           # build from cache/
python3 -m http.server -d _site 8765
```

`content/sitemap.json` 定义了分区、主题和仓库列表。手写页面位于 `content/pages/` 目录中。项目页面由各仓库的 README 经白名单 HTML 净化器处理后生成。若列表中包含私有仓库，或生成的任何页面颜色对比度低于 4.5:1，构建将会失败。

## 本地化

界面框架、导航、搜索和标签文本以 45 个语言环境发布，位于 `locales/` 目录下（20 个 Tier 1、15 个非洲和 10 个亚洲语言环境）。

- 静态 HTML 默认使用英语，可通过 `python3 build.py --lang <locale>` 构建任意语言环境版本。
- 页眉提供基于 `/assets/locales/*.json` 的语言切换器，支持浏览器语言自动检测，并为 RTL 语言环境（`ar`、`ar-EG`、`ar-MA`、`fa`、`he`、`ur`）提供 `dir="rtl"` 支持。
- 可使用 `python3 -m unittest discover -s tests` 在本地进行验证。

## 部署与许可证

`.github/workflows/pages.yml` 会在每次推送到 `main` 分支以及每天定时自动构建并部署到 GitHub Pages。请参阅[英文 README](../../../README.md) 和 [LICENSE](../../../LICENSE)。
