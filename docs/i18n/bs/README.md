> [English](../../../README.md)

# somethingwithproof.github.io

Izvorni kod za https://somethingwithproof.github.io: statička galerija javnih repozitorija sa automatski generisanim stranicama dokumentacije.

## Izgradnja

Zahtijeva Python 3.12 i GitHub CLI (`gh`), bez vanjskih Python zavisnosti:

```sh
python3 build.py --fetch   # refresh cache/ from GitHub, then build _site/
python3 build.py           # build from cache/
python3 -m http.server -d _site 8765
```

Datoteka `content/sitemap.json` definiše sekcije, teme i repozitorije. Ručno pisane stranice nalaze se u direktoriju `content/pages/`. Stranice projekata generišu se iz README datoteka repozitorija filtriranih kroz HTML čistač zasnovan na listi dozvoljenih elemenata. Izgradnja se zaustavlja ako je bilo koji navedeni repozitorij privatan ili ako odnos kontrasta boja padne ispod 4.5:1.

## Lokalizacija

Elementi interfejsa, navigacija, pretraga i oznake dostupni su u 48 jezičkih oznaka u direktoriju `locales/` (20 Tier 1, 15 afričkih, 10 azijskih i 3 južnoslavenske).

- Statični HTML podrazumijevano koristi engleski jezik i može se izgraditi za bilo koju podržanu jezičku oznaku pomoću `python3 build.py --lang <locale>`.
- Zaglavlje uključuje birač jezika zasnovan na `/assets/locales/*.json`, sa automatskim prepoznavanjem jezika preglednika i `dir="rtl"` podrškom za RTL jezike (`ar`, `ar-EG`, `ar-MA`, `fa`, `he`, `ur`).
- Provjerite lokalno pomoću `python3 -m unittest discover -s tests`.

## Postavljanje i licenca

Tok rada `.github/workflows/pages.yml` gradi i objavljuje stranicu na GitHub Pages pri svakom slanju na granu `main` i jednom dnevno. Pogledajte [englesku verziju README](../../../README.md) i datoteku [LICENSE](../../../LICENSE).
