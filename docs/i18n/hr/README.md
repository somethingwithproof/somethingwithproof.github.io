> [English](../../../README.md)

# somethingwithproof.github.io

Izvorni kod za https://somethingwithproof.github.io: statična galerija javnih repozitorija s automatski izrađenim stranicama dokumentacije.

## Izgradnja

Zahtijeva Python 3.12 i GitHub CLI (`gh`), bez vanjskih Python ovisnosti:

```sh
python3 build.py --fetch   # refresh cache/ from GitHub, then build _site/
python3 build.py           # build from cache/
python3 -m http.server -d _site 8765
```

Datoteka `content/sitemap.json` određuje odjeljke, teme i repozitorije. Ručno pisane stranice nalaze se u mapi `content/pages/`. Stranice projekata izrađuju se iz README datoteka repozitorija propuštenih kroz HTML pročišćivač temeljen na popisu dopuštenih elemenata. Izgradnja se prekida ako je bilo koji navedeni repozitorij privatan ili ako omjer kontrasta boja padne ispod 4.5:1.

## Lokalizacija

Dijelovi sučelja, navigacija, pretraživanje i natpisi dostupni su u 48 jezičnih oznaka u mapi `locales/` (20 Tier 1, 15 afričkih, 10 azijskih i 3 južnoslavenske).

- Statični HTML zadano koristi engleski jezik i može se izgraditi za bilo koju podržanu jezičnu oznaku naredbom `python3 build.py --lang <locale>`.
- Zaglavlje uključuje izbornik jezika temeljen na `/assets/locales/*.json`, s automatskim prepoznavanjem jezika preglednika i podrškom za `dir="rtl"` za RTL oznake (`ar`, `ar-EG`, `ar-MA`, `fa`, `he`, `ur`).
- Provjerite lokalno naredbom `python3 -m unittest discover -s tests`.

## Uvođenje i licencija

Tijek rada `.github/workflows/pages.yml` gradi i objavljuje web-mjesto na GitHub Pages pri svakom slanju na granu `main` te jednom dnevno. Pogledajte [englesku inačicu README](../../../README.md) i datoteku [LICENSE](../../../LICENSE).
