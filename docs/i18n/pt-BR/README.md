> [English](../../../README.md)

# somethingwithproof.github.io

Código-fonte de https://somethingwithproof.github.io: uma galeria estática de repositórios públicos com páginas de documentação geradas.

## Build

Requer Python 3.12 e a GitHub CLI (`gh`), sem dependências Python de terceiros:

```sh
python3 build.py --fetch   # refresh cache/ from GitHub, then build _site/
python3 build.py           # build from cache/
python3 -m http.server -d _site 8765
```

`content/sitemap.json` define seções, tópicos e repositórios. Páginas escritas manualmente ficam em `content/pages/`. As páginas de projeto são geradas a partir dos READMEs dos repositórios processados por um sanitizador de HTML baseado em lista de permissão. Os builds falham se algum repositório listado for privado ou se alguma razão de contraste de cor gerada ficar abaixo de 4.5:1.

## Localização

Os elementos de interface, navegação, busca e rótulos são distribuídos em 45 locales em `locales/` (20 Tier 1, 15 africanos e 10 asiáticos).

- O HTML estático usa inglês por padrão e pode ser gerado em qualquer locale via `python3 build.py --lang <locale>`.
- O cabeçalho oferece um seletor de idiomas baseado em `/assets/locales/*.json` com detecção automática do idioma do navegador e suporte a `dir="rtl"` para locales RTL (`ar`, `ar-EG`, `ar-MA`, `fa`, `he`, `ur`).
- Verifique localmente com `python3 -m unittest discover -s tests`.

## Deploy e Licença

`.github/workflows/pages.yml` faz o build e o deploy para o GitHub Pages a cada push para `main` e diariamente. Consulte o [README em inglês](../../../README.md) e [LICENSE](../../../LICENSE).
