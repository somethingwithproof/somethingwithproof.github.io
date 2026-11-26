> [English](../../../README.md)

# somethingwithproof.github.io

Código fuente de https://somethingwithproof.github.io: una galería estática de repositorios públicos con páginas de documentación generadas.

## Compilación

Requiere Python 3.12 y GitHub CLI (`gh`), sin dependencias de Python de terceros:

```sh
python3 build.py --fetch   # refresh cache/ from GitHub, then build _site/
python3 build.py           # build from cache/
python3 -m http.server -d _site 8765
```

`content/sitemap.json` define secciones, temas y repositorios. Las páginas escritas manualmente se encuentran en `content/pages/`. Las páginas de proyecto se generan a partir de los README de los repositorios procesados mediante un sanitizador HTML por lista de permitidos. Las compilaciones fallan si alguno de los repositorios listados es privado o si cualquier relación de contraste de color generada desciende por debajo de 4.5:1.

## Localización

Los elementos de la interfaz, la navegación, la búsqueda y las etiquetas se distribuyen en 45 configuraciones regionales bajo `locales/` (20 de nivel 1, 15 africanas y 10 asiáticas).

- El HTML estático utiliza el inglés de forma predeterminada y puede compilarse en cualquier configuración regional mediante `python3 build.py --lang <locale>`.
- El encabezado ofrece un selector de idioma respaldado por `/assets/locales/*.json` con detección automática del idioma del navegador y compatibilidad con `dir="rtl"` para configuraciones regionales RTL (`ar`, `ar-EG`, `ar-MA`, `fa`, `he`, `ur`).
- Verifica localmente con `python3 -m unittest discover -s tests`.

## Despliegue y licencia

`.github/workflows/pages.yml` compila y despliega en GitHub Pages en cada push a `main` y de forma diaria. Consulta el [README completo en inglés](../../../README.md) y [LICENSE](../../../LICENSE).
