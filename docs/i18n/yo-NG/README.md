> [English](../../../README.md)

# somethingwithproof.github.io

Orísun fún https://somethingwithproof.github.io: ibi-ìfihàn aláìyípadà ti àwọn ibi-ìpamọ́ gbogbogbòò pẹ̀lú àwọn ojú-ewé ìwé-àkọsílẹ̀ tí a ṣẹ̀dá.

## Ìkọ́lé

Ó nílò Python 3.12 àti GitHub CLI (`gh`), láìsí ìgbẹ́kẹ̀lé Python láti ọ̀dọ̀ ẹni-kẹta:

```sh
python3 build.py --fetch   # refresh cache/ from GitHub, then build _site/
python3 build.py           # build from cache/
python3 -m http.server -d _site 8765
```

`content/sitemap.json` ń ṣàlàyé àwọn apá, àwọn kókó-ọ̀rọ̀, àti àwọn ibi-ìpamọ́. Àwọn ojú-ewé tí a kọ́ fúnra ẹni wà nínú `content/pages/`. A ń ṣẹ̀dá àwọn ojú-ewé iṣẹ́-àkànṣe láti inú README àwọn ibi-ìpamọ́ tí a gbé gba inú olùṣàlẹ̀mọ́ HTML tí ó ní àkójọ ìfàyègbà. Ìkọ́lé máa ń kùnà bí ibi-ìpamọ́ èyíkéyìí tí a kọ sílẹ̀ bá jẹ́ àdáni tàbí bí ìpín ìyàtọ̀ àwọ̀ èyíkéyìí tí a ṣẹ̀dá bá wálẹ̀ sí ìsàlẹ̀ 4.5:1.

## Ìsọdèdè-agbègbè

Ètò ojú-òpó UI, ìtọ́sọ́nà, ìwádìí, àti àwọn àmì-ìdámọ̀ ń jáde ní èdè agbègbè 45 lábẹ́ `locales/` (20 ti Ìpele 1, 15 ti Áfíríkà, àti 10 ti Éṣíà).

- HTML aláìyípadà ń bẹ̀rẹ̀ ní èdè Gẹ̀ẹ́sì, a sì lè kọ́ ọ ní èdè agbègbè èyíkéyìí nípasẹ̀ `python3 build.py --lang <locale>`.
- Àkọlé náà ń pèsè olùyípadà èdè tí `/assets/locales/*.json` ń ṣe àtìlẹ́yìn fún pẹ̀lú ìwárí èdè aṣàwárí aládàáni àti àtìlẹ́yìn `dir="rtl"` fún àwọn èdè agbègbè RTL (`ar`, `ar-EG`, `ar-MA`, `fa`, `he`, `ur`).
- Ṣe ìdánilójú lórí ẹ̀rọ rẹ pẹ̀lú `python3 -m unittest discover -s tests`.

## Ìfìsílẹ̀-iṣẹ́ àti Ìwé-àṣẹ

`.github/workflows/pages.yml` ń kọ́, ó sì ń fi sílẹ̀ sí GitHub Pages lórí gbogbo ìtìsókè sí `main` àti lójoojúmọ́. Wo [README èdè Gẹ̀ẹ́sì](../../../README.md) àti [LICENSE](../../../LICENSE).
