> [English](../../../README.md)

# somethingwithproof.github.io

Inkomoko ya https://somethingwithproof.github.io: urubuga rudahinduka rw'ububiko rusange rufite impapuro z'inyandiko zakozwe mu buryo bwikora.

## Kubaka

Bisaba Python 3.12 na GitHub CLI (`gh`), nta bindi bikoresho bya Python byo ku ruhande bikenewe:

```sh
python3 build.py --fetch   # refresh cache/ from GitHub, then build _site/
python3 build.py           # build from cache/
python3 -m http.server -d _site 8765
```

`content/sitemap.json` isobanura ibice, insanganyamatsiko, n'ububiko. Impapuro zanditswe n'intoki ziri muri `content/pages/`. Impapuro z'imishinga zikorwa zivuye muri za README z'ububiko zinyujijwe muri sanitizer ya HTML ifite urutonde rw'ibyemewe. Kubaka birahagarara iyo hari ububiko bwihishe buri ku rutonde cyangwa iyo igipimo cy'itandukaniro ry'amabara cyakozwe kigiye munsi ya 4.5:1.

## Ishyirwa mu ndimi

Imigaragarire ya UI, uburyo bwo kuyoborwa, ishakisha, n'ibirango bitangwa mu ndimi 45 munsi ya `locales/` (indimi 20 z'icyiciro cya 1, 15 zo muri Afurika, na 10 zo muri Aziya).

- HTML idahinduka ihera ku Cyongereza kandi ishobora kubakwa mu rurimi urwo ari rwo rwose hakoreshejwe `python3 build.py --lang <locale>`.
- Umutwe utanga uburyo bwo guhindura ururimi bushingiye kuri `/assets/locales/*.json` bufite ubugenzuzi bwikora bw'ururimi rwa mushakisha n'ubufasha bwa `dir="rtl"` ku ndimi za RTL (`ar`, `ar-EG`, `ar-MA`, `fa`, `he`, `ur`).
- Genzura kuri mudasobwa yawe ukoresheje `python3 -m unittest discover -s tests`.

## Ishyira hanze n'Uruhushya

`.github/workflows/pages.yml` yubaka kandi igashyira kuri GitHub Pages kuri buri push kuri `main` na buri munsi. Reba [README yuzuye mu Cyongereza](../../../README.md) na [LICENSE](../../../LICENSE).
