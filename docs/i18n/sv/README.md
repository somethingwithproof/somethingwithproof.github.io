> [English](../../../README.md)

# somethingwithproof.github.io

Källkod för https://somethingwithproof.github.io: ett statiskt galleri över publika arkiv med genererade dokumentationssidor.

## Bygge

Kräver Python 3.12 och GitHub CLI (`gh`), utan Python-beroenden från tredje part:

```sh
python3 build.py --fetch   # refresh cache/ from GitHub, then build _site/
python3 build.py           # build from cache/
python3 -m http.server -d _site 8765
```

`content/sitemap.json` definierar sektioner, ämnen och arkiv. Handskrivna sidor finns i `content/pages/`. Projektsidor genereras från arkivens README-filer som körs genom en HTML-sanerare med tillåtelselista. Byggen misslyckas om något listat arkiv är privat eller om något genererat färgkontrastförhållande sjunker under 4.5:1.

## Lokalisering

Gränssnittsramar, navigering, sökning och etiketter levereras på 45 språkområden under `locales/` (20 Tier 1-, 15 afrikanska och 10 asiatiska språkområden).

- Statisk HTML använder engelska som standard och kan byggas för valfritt språkområde via `python3 build.py --lang <locale>`.
- Sidhuvudet har en språkväljare som stöds av `/assets/locales/*.json` med automatisk identifiering av webbläsarspråk och `dir="rtl"`-stöd för RTL-språkområden (`ar`, `ar-EG`, `ar-MA`, `fa`, `he`, `ur`).
- Verifiera lokalt med `python3 -m unittest discover -s tests`.

## Driftsättning och licens

`.github/workflows/pages.yml` bygger och driftsätter till GitHub Pages vid varje push till `main` samt dagligen. Se den [engelska README-filen](../../../README.md) och [LICENSE](../../../LICENSE).
