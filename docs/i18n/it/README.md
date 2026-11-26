> [English](../../../README.md)

# somethingwithproof.github.io

Sorgenti di https://somethingwithproof.github.io: una galleria statica di repository pubblici con pagine di documentazione generate.

## Build

Richiede Python 3.12 e la GitHub CLI (`gh`), senza dipendenze Python di terze parti:

```sh
python3 build.py --fetch   # refresh cache/ from GitHub, then build _site/
python3 build.py           # build from cache/
python3 -m http.server -d _site 8765
```

`content/sitemap.json` definisce sezioni, argomenti e repository. Le pagine scritte manualmente si trovano in `content/pages/`. Le pagine dei progetti vengono generate dai README dei repository filtrati attraverso un sanitizer HTML a allowlist. La build fallisce se uno qualsiasi dei repository elencati è privato o se il rapporto di contrasto di qualsiasi colore generato scende sotto 4.5:1.

## Localizzazione

Interfaccia utente, navigazione, ricerca ed etichette sono distribuite in 45 localizzazioni in `locales/` (20 Tier 1, 15 africane e 10 asiatiche).

- L'HTML statico usa l'inglese come lingua predefinita e può essere generato in qualsiasi localizzazione tramite `python3 build.py --lang <locale>`.
- L'intestazione offre un selettore della lingua supportato da `/assets/locales/*.json` con rilevamento automatico della lingua del browser e supporto `dir="rtl"` per le localizzazioni RTL (`ar`, `ar-EG`, `ar-MA`, `fa`, `he`, `ur`).
- Verifica in locale con `python3 -m unittest discover -s tests`.

## Deploy e licenza

`.github/workflows/pages.yml` compila ed esegue il deploy su GitHub Pages a ogni push su `main` e quotidianamente. Consulta il [README completo in inglese](../../../README.md) e [LICENSE](../../../LICENSE).
