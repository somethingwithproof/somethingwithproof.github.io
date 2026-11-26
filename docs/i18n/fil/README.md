> [English](../../../README.md)

# somethingwithproof.github.io

Source para sa https://somethingwithproof.github.io: isang static na gallery ng mga pampublikong repository na may mga nabuong pahina ng dokumentasyon.

## Pag-build

Nangangailangan ng Python 3.12 at ng GitHub CLI (`gh`), na walang third-party na Python dependency:

```sh
python3 build.py --fetch   # refresh cache/ from GitHub, then build _site/
python3 build.py           # build from cache/
python3 -m http.server -d _site 8765
```

Tinutukoy ng `content/sitemap.json` ang mga seksyon, paksa, at repository. Nakalagay ang mga hand-written na pahina sa `content/pages/`. Binubuo ang mga pahina ng proyekto mula sa mga README ng repository na ipinapadaan sa isang allowlist HTML sanitizer. Nabibigo ang pag-build kung pribado ang alinmang nakalistang repository o kung bumaba sa 4.5:1 ang alinmang nabuong contrast ratio ng kulay.

## Lokalisasyon

Ipinapadala ang UI chrome, nabigasyon, paghahanap, at mga label sa 45 locale sa ilalim ng `locales/` (20 Tier 1, 15 African, at 10 Asian na locale).

- Naka-default sa Ingles ang static na HTML at maaaring i-build sa alinmang locale sa pamamagitan ng `python3 build.py --lang <locale>`.
- Nagbibigay ang header ng tagapagpalit ng wika na sinusuportahan ng `/assets/locales/*.json` na may awtomatikong pagtukoy ng wika ng browser at suporta sa `dir="rtl"` para sa mga RTL na locale (`ar`, `ar-EG`, `ar-MA`, `fa`, `he`, `ur`).
- Patunayan nang lokal gamit ang `python3 -m unittest discover -s tests`.

## Pag-deploy at Lisensya

Nagbi-build at nagde-deploy ang `.github/workflows/pages.yml` sa GitHub Pages sa bawat push sa `main` at araw-araw. Tingnan ang [README sa Ingles](../../../README.md) at [LICENSE](../../../LICENSE).
