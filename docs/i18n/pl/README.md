> [English](../../../README.md)

# somethingwithproof.github.io

Kod źródłowy witryny https://somethingwithproof.github.io: statycznej galerii publicznych repozytoriów z automatycznie generowanymi stronami dokumentacji.

## Budowanie

Wymaga Pythona 3.12 oraz GitHub CLI (`gh`), bez zewnętrznych zależności Pythona:

```sh
python3 build.py --fetch   # refresh cache/ from GitHub, then build _site/
python3 build.py           # build from cache/
python3 -m http.server -d _site 8765
```

Plik `content/sitemap.json` definiuje sekcje, tematy i repozytoria. Strony tworzone ręcznie znajdują się w katalogu `content/pages/`. Strony projektów są generowane na podstawie plików README repozytoriów przepuszczonych przez oczyszczacz HTML oparty na liście dozwolonych elementów. Budowanie kończy się błędem, jeśli którekolwiek z wymienionych repozytoriów jest prywatne lub jeśli współczynnik kontrastu kolorów spadnie poniżej 4.5:1.

## Lokalizacja

Elementy interfejsu, nawigacja, wyszukiwarka i etykiety są dostępne w 45 ustawieniach regionalnych w katalogu `locales/` (20 z grupy Tier 1, 15 afrykańskich i 10 azjatyckich).

- Statyczny kod HTML używa domyślnie języka angielskiego i można go zbudować dla dowolnego języka za pomocą polecenia `python3 build.py --lang <locale>`.
- Nagłówek udostępnia przełącznik języka korzystający z plików `/assets/locales/*.json`, z automatycznym wykrywaniem języka przeglądarki oraz obsługą `dir="rtl"` dla ustawień regionalnych RTL (`ar`, `ar-EG`, `ar-MA`, `fa`, `he`, `ur`).
- Zweryfikuj lokalnie poleceniem `python3 -m unittest discover -s tests`.

## Wdrażanie i licencja

Przepływ pracy `.github/workflows/pages.yml` buduje i wdraża witrynę w GitHub Pages przy każdym wypchnięciu zmian do gałęzi `main` oraz codziennie. Zobacz [angielską wersję README](../../../README.md) oraz plik [LICENSE](../../../LICENSE).
