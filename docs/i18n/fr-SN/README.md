> [English](../../../README.md)

# somethingwithproof.github.io

Code source de https://somethingwithproof.github.io : une galerie statique de dépôts publics avec des pages de documentation générées.

## Construction

Nécessite Python 3.12 et la CLI GitHub (`gh`), sans aucune dépendance Python tierce :

```sh
python3 build.py --fetch   # refresh cache/ from GitHub, then build _site/
python3 build.py           # build from cache/
python3 -m http.server -d _site 8765
```

`content/sitemap.json` définit les sections, les sujets et les dépôts. Les pages rédigées manuellement se trouvent dans `content/pages/`. Les pages de projet sont générées à partir des README des dépôts passés par un filtre HTML à liste d'autorisation. La compilation échoue si un dépôt répertorié est privé ou si le rapport de contraste des couleurs généré descend sous 4.5:1.

## Localisation

L'interface utilisateur, la navigation, la recherche et les libellés sont fournis dans 45 paramètres régionaux sous `locales/` (20 de niveau 1, 15 africains et 10 asiatiques).

- Le HTML statique utilise l'anglais par défaut et peut être généré dans n'importe quel paramètre régional via `python3 build.py --lang <locale>`.
- L'en-tête propose un sélecteur de langue alimenté par `/assets/locales/*.json` avec détection automatique de la langue du navigateur et prise en charge de `dir="rtl"` pour les paramètres régionaux RTL (`ar`, `ar-EG`, `ar-MA`, `fa`, `he`, `ur`).
- Vérifiez localement avec `python3 -m unittest discover -s tests`.

## Déploiement et licence

`.github/workflows/pages.yml` compile et déploie sur GitHub Pages à chaque push sur `main` ainsi que quotidiennement. Consultez le [README complet en anglais](../../../README.md) et le fichier [LICENSE](../../../LICENSE).
