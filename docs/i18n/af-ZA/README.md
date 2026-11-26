> [English](../../../README.md)

# somethingwithproof.github.io

Bronkode vir https://somethingwithproof.github.io: 'n statiese galery van openbare bewaarplekke met gegenereerde dokumentasiebladsye.

## Bou

Vereis Python 3.12 en die GitHub CLI (`gh`), sonder enige derdeparty-Python-afhanklikhede:

```sh
python3 build.py --fetch   # refresh cache/ from GitHub, then build _site/
python3 build.py           # build from cache/
python3 -m http.server -d _site 8765
```

`content/sitemap.json` definieer afdelings, onderwerpe en bewaarplekke. Handgeskrewe bladsye lê in `content/pages/`. Projekbladsye word gegenereer uit bewaarplek-README's wat deur 'n toelaatlys-HTML-saniteerder gestuur word. Bouprosesse faal indien enige gelyste bewaarplek privaat is of indien enige gegenereerde kleurkontrasverhouding onder 4.5:1 daal.

## Lokalisering

Koppelvlakelemente, navigasie, soektog en etikette word in 45 locales onder `locales/` (20 Vlak 1-, 15 Afrika- en 10 Asiatiese locales) verskeep.

- Statiese HTML gebruik standaard Engels en kan in enige locale gebou word via `python3 build.py --lang <locale>`.
- Die kopstuk bied 'n taalskakelaar gerugsteun deur `/assets/locales/*.json` met outomatiese blaaier-taalbespeuring en `dir="rtl"`-ondersteuning vir RTL-locales (`ar`, `ar-EG`, `ar-MA`, `fa`, `he`, `ur`).
- Verifieer plaaslik met `python3 -m unittest discover -s tests`.

## Ontplooiing en lisensie

`.github/workflows/pages.yml` bou en ontplooi na GitHub Pages met elke push na `main` en daagliks. Sien die [Engelse README](../../../README.md) en [LICENSE](../../../LICENSE).
