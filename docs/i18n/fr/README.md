> [English](../../../README.md)

# somethingwithproof.github.io

Sources de https://somethingwithproof.github.io : une galerie statique de dépôts publics accompagnée de pages de documentation générées.

## Génération

Nécessite Python 3.12 et la CLI GitHub (`gh`), sans aucune dépendance Python tierce :

```sh
python3 build.py --fetch   # refresh cache/ from GitHub, then build _site/
python3 build.py           # build from cache/
python3 -m http.server -d _site 8765
```

`content/sitemap.json` définit les sections, les thèmes et les dépôts. Les pages rédigées manuellement se trouvent dans `content/pages/`. Les pages de projet sont générées à partir des README des dépôts filtrés par un nettoyeur HTML à liste d'autorisation. La génération échoue si l'un des dépôts répertoriés est privé ou si un ratio de contraste des couleurs généré descend sous 4,5:1.

## Localisation

L'interface, la navigation, la recherche et les libellés sont fournis en 45 locales dans `locales/` (20 de niveau 1, 15 africaines et 10 asiatiques).

- Le HTML statique utilise l'anglais par défaut et peut être généré dans n'importe quelle locale via `python3 build.py --lang <locale>`.
- L'en-tête propose un sélecteur de langue alimenté par `/assets/locales/*.json` avec détection automatique de la langue du navigateur et prise en charge de `dir="rtl"` pour les locales RTL (`ar`, `ar-EG`, `ar-MA`, `fa`, `he`, `ur`).
- Vérifiez localement avec `python3 -m unittest discover -s tests`.

## Déploiement et licence

`.github/workflows/pages.yml` génère et déploie le site sur GitHub Pages à chaque push sur `main` ainsi que quotidiennement. Consultez le [README anglais](../../../README.md) et [LICENSE](../../../LICENSE).
