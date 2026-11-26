> [English](../../../README.md)

# somethingwithproof.github.io

Broncode voor https://somethingwithproof.github.io: een statische galerij van openbare repositories met gegenereerde documentatiepagina's.

## Bouwen

Vereist Python 3.12 en de GitHub CLI (`gh`), zonder Python-afhankelijkheden van derden:

```sh
python3 build.py --fetch   # refresh cache/ from GitHub, then build _site/
python3 build.py           # build from cache/
python3 -m http.server -d _site 8765
```

`content/sitemap.json` definieert secties, onderwerpen en repositories. Handgeschreven pagina's staan in `content/pages/`. Projectpagina's worden gegenereerd uit README's van repositories die door een HTML-sanitizer op basis van een allowlist worden gehaald. De build mislukt als een vermelde repository privé is of als een gegenereerde kleurcontrastverhouding onder 4,5:1 zakt.

## Lokalisatie

UI-elementen, navigatie, zoekfunctie en labels worden geleverd in 45 locales onder `locales/` (20 Tier 1-, 15 Afrikaanse en 10 Aziatische locales).

- Statische HTML gebruikt standaard Engels en kan in elke locale worden gebouwd via `python3 build.py --lang <locale>`.
- De koptekst biedt een taalkiezer op basis van `/assets/locales/*.json` met automatische taaldetectie in de browser en `dir="rtl"`-ondersteuning voor RTL-locales (`ar`, `ar-EG`, `ar-MA`, `fa`, `he`, `ur`).
- Controleer lokaal met `python3 -m unittest discover -s tests`.

## Implementatie en licentie

`.github/workflows/pages.yml` bouwt en implementeert naar GitHub Pages bij elke push naar `main` en dagelijks. Zie de [Engelse README](../../../README.md) en [LICENSE](../../../LICENSE).
