> [English](../../../README.md)

# somethingwithproof.github.io

Msimbo chanzo wa https://somethingwithproof.github.io: ghala tuli la hazina za umma lenye kurasa za nyaraka zilizoundwa kiotomatiki.

## Ujenzi

Inahitaji Python 3.12 na GitHub CLI (`gh`), bila utegemezi wowote wa Python kutoka kwa wahusika wengine:

```sh
python3 build.py --fetch   # refresh cache/ from GitHub, then build _site/
python3 build.py           # build from cache/
python3 -m http.server -d _site 8765
```

`content/sitemap.json` hufafanua sehemu, mada, na hazina. Kurasa zilizoandikwa kwa mkono ziko katika `content/pages/`. Kurasa za mradi huundwa kutoka kwa faili za README za hazina zilizopitishwa kwenye kisafishaji cha HTML kinachotumia orodha ya ruhusa. Ujenzi hushindwa ikiwa hazina yoyote iliyoorodheshwa ni ya faragha au ikiwa uwiano wowote wa utofautishaji wa rangi ulioundwa unashuka chini ya 4.5:1.

## Ujanibishaji

Vipengele vya kiolesura, urambazaji, utafutaji, na lebo hutolewa katika lugha na maeneo 45 chini ya `locales/` (maeneo 20 ya Daraja la 1, 15 ya Afrika, na 10 ya Asia).

- HTML tuli hutumia Kiingereza kama chaguo-msingi na inaweza kujengwa katika eneo lolote kupitia `python3 build.py --lang <locale>`.
- Kichwa cha ukurasa hutoa kibadilisha lugha kinachoungwa mkono na `/assets/locales/*.json` chenye utambuzi wa kiotomatiki wa lugha ya kivinjari na usaidizi wa `dir="rtl"` kwa maeneo ya RTL (`ar`, `ar-EG`, `ar-MA`, `fa`, `he`, `ur`).
- Thibitisha kwenye mashine yako kwa kutumia `python3 -m unittest discover -s tests`.

## Upelekaji na Leseni

`.github/workflows/pages.yml` hujenga na kupeleka kwenye GitHub Pages kila mara mabadiliko yanapotumwa kwenye `main` na kila siku. Tazama [README ya Kiingereza](../../../README.md) na [LICENSE](../../../LICENSE).
