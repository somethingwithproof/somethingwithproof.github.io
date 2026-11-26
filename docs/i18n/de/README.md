> [English](../../../README.md)

# somethingwithproof.github.io

Quellcode für https://somethingwithproof.github.io: eine statische Galerie öffentlicher Repositories mit generierten Dokumentationsseiten.

## Build

Erfordert Python 3.12 und die GitHub CLI (`gh`), ohne Python-Abhängigkeiten von Drittanbietern:

```sh
python3 build.py --fetch   # refresh cache/ from GitHub, then build _site/
python3 build.py           # build from cache/
python3 -m http.server -d _site 8765
```

`content/sitemap.json` definiert Abschnitte, Themen und Repositories. Handgeschriebene Seiten liegen unter `content/pages/`. Projektseiten werden aus Repository-READMEs generiert, die einen Allowlist-basierten HTML-Sanitizer durchlaufen. Builds schlagen fehl, wenn ein aufgeführtes Repository privat ist oder das generierte Farbkontrastverhältnis unter 4,5:1 fällt.

## Lokalisierung

UI-Elemente, Navigation, Suche und Beschriftungen werden in 45 Locales unter `locales/` ausgeliefert (20 Tier-1-, 15 afrikanische und 10 asiatische Locales).

- Statisches HTML ist standardmäßig auf Englisch und lässt sich über `python3 build.py --lang <locale>` für jedes beliebige Locale erzeugen.
- Die Kopfzeile bietet einen Sprachumschalter auf Basis von `/assets/locales/*.json` mit automatischer Browsersprachen-Erkennung und `dir="rtl"`-Unterstützung für RTL-Locales (`ar`, `ar-EG`, `ar-MA`, `fa`, `he`, `ur`).
- Lokal überprüfen mit `python3 -m unittest discover -s tests`.

## Bereitstellung und Lizenz

`.github/workflows/pages.yml` baut und veröffentlicht die Seite bei jedem Push auf `main` sowie täglich auf GitHub Pages. Siehe die [englische README](../../../README.md) und [LICENSE](../../../LICENSE).
