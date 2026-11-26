> [English](../../../README.md)

# somethingwithproof.github.io

Isha loogu talagalay https://somethingwithproof.github.io: bandhig joogto ah oo kaydadka dadweynaha ah oo leh bogag dukumiinti oo la soo saaray.

## Dhisidda

Waxay u baahan tahay Python 3.12 iyo GitHub CLI (`gh`), iyadoo aan lahayn wax ku-tiirsanaan Python oo dhinac saddexaad ah:

```sh
python3 build.py --fetch   # refresh cache/ from GitHub, then build _site/
python3 build.py           # build from cache/
python3 -m http.server -d _site 8765
```

`content/sitemap.json` wuxuu qeexaa qaybaha, mowduucyada, iyo kaydadka. Boggaga gacanta lagu qoray waxay ku jiraan `content/pages/`. Boggaga mashaariicda waxaa laga soo saaraa README-yada kaydadka oo la mariyay nadiifiye HTML oo liis oggolaansho leh. Dhisiddu way fashilantaa haddii kayd kasta oo ku qoran uu yahay mid gaar ah ama haddii saamiga isbarbardhigga midabka ee la soo saaray uu ka hoos maro 4.5:1.

## Deegaameynta

Qalabka UI, hagidda, raadinta, iyo calaamadaha waxay ku yimaadaan 45 deegaan oo ku hoos jira `locales/` (20 Heerka 1-aad, 15 Afrikaan, iyo 10 Aasiyaan ah).

- HTML-ka joogtada ah wuxuu si caadi ah u adeegsadaa Ingiriis waxaana lagu dhisi karaa deegaan kasta iyadoo la adeegsanayo `python3 build.py --lang <locale>`.
- Madaxa sare wuxuu bixiyaa beddelaha luqadda oo ay taageerto `/assets/locales/*.json` oo leh ogaanshaha tooska ah ee luqadda biraawsarka iyo taageerada `dir="rtl"` ee deegaannada RTL (`ar`, `ar-EG`, `ar-MA`, `fa`, `he`, `ur`).
- Ku xaqiiji maxalli ahaan adigoo adeegsanaya `python3 -m unittest discover -s tests`.

## Daabulidda iyo Shatiga

`.github/workflows/pages.yml` wuxuu dhisaa oo u daabulaa GitHub Pages riix kasta oo lagu sameeyo `main` iyo maalin kasta. Eeg [README-ga Ingiriisiga](../../../README.md) oo dhammaystiran iyo [LICENSE](../../../LICENSE).
