> [English](../../../README.md)

# somethingwithproof.github.io

Loharano ho an'ny https://somethingwithproof.github.io: toeram-pampirantiana tsy miovaova ho an'ny tahiry ho an'ny daholobe miaraka amin'ny pejy tahirin-kevitra novokarina.

## Fanamboarana

Mitaky Python 3.12 sy GitHub CLI (`gh`), tsy misy fiankinan-doha Python avy amin'ny antoko fahatelo:

```sh
python3 build.py --fetch   # refresh cache/ from GitHub, then build _site/
python3 build.py           # build from cache/
python3 -m http.server -d _site 8765
```

`content/sitemap.json` dia mamaritra ny fizarana, ny lohahevitra, ary ny tahiry. Ireo pejy nosoratana tanana dia mipetraka ao amin'ny `content/pages/`. Ireo pejin'ny tetikasa dia vokarina avy amin'ny README an'ny tahiry nandalo mpanadio HTML mifototra amin'ny lisitra nahazo alalana. Tsy mahomby ny fanamboarana raha tsy ho an'ny daholobe ny iray amin'ireo tahiry voatanisa na raha midina ambanin'ny 4.5:1 ny tahan'ny fifanoheran'ny loko novokarina.

## Fampifanarahana amin'ny fiteny

Ny rafitry ny UI, ny fitetezana, ny fikarohana, ary ny marika dia omena amin'ny fiteny eo an-toerana miisa 45 ao ambanin'ny `locales/` (fiteny sokajy 1 miisa 20, fiteny afrikanina miisa 15, ary fiteny aziatika miisa 10).

- Ny HTML tsy miovaova dia mampiasa ny teny anglisy amin'ny fomba mahazatra ary azo amboarina amin'ny fiteny eo an-toerana rehetra amin'ny alalan'ny `python3 build.py --lang <locale>`.
- Ny lohan'ny pejy dia manome mpanova fiteny tohanan'ny `/assets/locales/*.json` miaraka amin'ny famantarana mandeha ho azy ny fitenin'ny mpitety tranonkala sy fanohanana `dir="rtl"` ho an'ny fiteny RTL (`ar`, `ar-EG`, `ar-MA`, `fa`, `he`, `ur`).
- Hamarino eo an-toerana amin'ny alalan'ny `python3 -m unittest discover -s tests`.

## Fametrahana sy Lisansa

`.github/workflows/pages.yml` dia manamboatra sy mametraka ao amin'ny GitHub Pages isaky ny misy fandefasana mankany amin'ny `main` sy isan'andro. Jereo ny [README amin'ny teny anglisy](../../../README.md) sy ny [LICENSE](../../../LICENSE).
