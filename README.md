# somethingwithproof.github.io

**Languages:** **English** · [Deutsch](docs/i18n/de/README.md) · [Español](docs/i18n/es/README.md) · [Français](docs/i18n/fr/README.md) · [Português (BR)](docs/i18n/pt-BR/README.md) · [日本語](docs/i18n/ja/README.md) · [한국어](docs/i18n/ko/README.md) · [简体中文](docs/i18n/zh-CN/README.md) · [العربية](docs/i18n/ar/README.md) · [हिन्दी](docs/i18n/hi/README.md)

<details>
<summary>All 48 languages</summary>

**Tier 1:** **English** · [Deutsch](docs/i18n/de/README.md) · [Español](docs/i18n/es/README.md) · [Français](docs/i18n/fr/README.md) · [Italiano](docs/i18n/it/README.md) · [Português (BR)](docs/i18n/pt-BR/README.md) · [Nederlands](docs/i18n/nl/README.md) · [Русский](docs/i18n/ru/README.md) · [Українська](docs/i18n/uk/README.md) · [日本語](docs/i18n/ja/README.md) · [한국어](docs/i18n/ko/README.md) · [简体中文](docs/i18n/zh-CN/README.md) · [繁體中文](docs/i18n/zh-TW/README.md) · [العربية](docs/i18n/ar/README.md) · [हिन्दी](docs/i18n/hi/README.md) · [Polski](docs/i18n/pl/README.md) · [Türkçe](docs/i18n/tr/README.md) · [Svenska](docs/i18n/sv/README.md) · [Tiếng Việt](docs/i18n/vi/README.md) · [Bahasa Indonesia](docs/i18n/id/README.md)

**African:** [Afrikaans (ZA)](docs/i18n/af-ZA/README.md) · [አማርኛ (ET)](docs/i18n/am-ET/README.md) · [العربية (مصر)](docs/i18n/ar-EG/README.md) · [العربية (المغرب)](docs/i18n/ar-MA/README.md) · [Français (MA)](docs/i18n/fr-MA/README.md) · [Français (SN)](docs/i18n/fr-SN/README.md) · [Hausa (NG)](docs/i18n/ha-NG/README.md) · [Igbo (NG)](docs/i18n/ig-NG/README.md) · [Malagasy (MG)](docs/i18n/mg-MG/README.md) · [Kinyarwanda (RW)](docs/i18n/rw-RW/README.md) · [Soomaali (SO)](docs/i18n/so-SO/README.md) · [Kiswahili (KE)](docs/i18n/sw-KE/README.md) · [isiXhosa (ZA)](docs/i18n/xh-ZA/README.md) · [Yorùbá (NG)](docs/i18n/yo-NG/README.md) · [isiZulu (ZA)](docs/i18n/zu-ZA/README.md)

**Asian:** [বাংলা](docs/i18n/bn/README.md) · [فارسی](docs/i18n/fa/README.md) · [עברית](docs/i18n/he/README.md) · [मराठी](docs/i18n/mr/README.md) · [தமிழ்](docs/i18n/ta/README.md) · [తెలుగు](docs/i18n/te/README.md) · [ไทย](docs/i18n/th/README.md) · [اردو](docs/i18n/ur/README.md) · [Bahasa Melayu](docs/i18n/ms/README.md) · [Filipino](docs/i18n/fil/README.md)

**South Slavic:** [Bosanski](docs/i18n/bs/README.md) · [Hrvatski](docs/i18n/hr/README.md) · [Српски](docs/i18n/sr/README.md)

</details>

Source for https://somethingwithproof.github.io: a gallery of public projects with a documentation page for each repository.

## Build

Python 3.12 and the GitHub CLI, no other dependencies.

```sh
python3 build.py --fetch   # refresh cache/ from GitHub, then build _site/
python3 build.py           # build from cache/
python3 -m http.server -d _site 8765
```

`content/sitemap.json` defines the sections, topics and which repositories appear. Hand-written pages live in `content/pages/`. Project pages are generated from each repository's README, filtered through an allowlist sanitizer.

Mermaid diagrams in READMEs and documents are drawn in the browser by a copy of Mermaid served from this site. The build downloads the pinned npm release once, checks it against the registry's sha512, and stops if the hash does not match. To upgrade, change `MERMAID_VERSION` and `MERMAID_INTEGRITY` in `build.py`.

The build stops if a listed repository is private, or if any text colour pair falls below 4.5:1 contrast.

## Localization

UI chrome, navigation, search, and labels ship in 48 locales under `locales/`: 20 Tier 1 (`en`, `de`, `es`, `fr`, `it`, `pt-BR`, `nl`, `ru`, `uk`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ar`, `hi`, `pl`, `tr`, `sv`, `vi`, `id`), 15 African (`af-ZA`, `am-ET`, `ar-EG`, `ar-MA`, `fr-MA`, `fr-SN`, `ha-NG`, `ig-NG`, `mg-MG`, `rw-RW`, `so-SO`, `sw-KE`, `xh-ZA`, `yo-NG`, `zu-ZA`), 10 Asian (`bn`, `fa`, `he`, `mr`, `ta`, `te`, `th`, `ur`, `ms`, `fil`), and 3 South Slavic (`bs`, `hr`, `sr`).

- Static HTML defaults to English and can be built in any supported locale via `python3 build.py --lang <locale>`.
- The header includes a language switcher backed by `/assets/locales/*.json` with browser language auto-detection and `<html lang="..." dir="rtl">` for RTL locales (`ar`, `ar-EG`, `ar-MA`, `fa`, `he`, `ur`).
- Localized READMEs for all 47 non-English locales live under `docs/i18n/<locale>/README.md`.
- Run `python3 -m unittest discover -s tests` to verify locale parity and build output.

## Deploy

`.github/workflows/pages.yml` builds and deploys on every push to `main` and once a day.
