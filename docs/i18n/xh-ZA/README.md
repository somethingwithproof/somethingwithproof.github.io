> [English](../../../README.md)

# somethingwithproof.github.io

Umthombo we-https://somethingwithproof.github.io: igalari engaguqukiyo yeendawo zokugcina ikhowudi ezisesidlangalaleni ezinamaphepha amaxwebhu avelisiweyo.

## Ukwakha

Ifuna i-Python 3.12 kunye ne-GitHub CLI (`gh`), ngaphandle kokuxhomekeka kwe-Python yomntu wesithathu:

```sh
python3 build.py --fetch   # refresh cache/ from GitHub, then build _site/
python3 build.py           # build from cache/
python3 -m http.server -d _site 8765
```

I-`content/sitemap.json` ichaza amacandelo, izihloko, kunye neendawo zokugcina ikhowudi. Amaphepha abhalwe ngesandla ahlala kwi-`content/pages/`. Amaphepha eeprojekthi aveliswa kwii-README zeendawo zokugcina ikhowudi ezidluliswe kwisihlambululi se-HTML soluhlu lwamavume. Ukwakha kuyasilela ukuba nayiphi na indawo yokugcina ikhowudi edwelisiweyo iyimfihlo okanye ukuba nawuphi na umlinganiselo womahluko wemibala ovelisiweyo wehla ngaphantsi kwe-4.5:1.

## Ulungiselelo lweelwimi

I-UI chrome, ukuhamba, ukukhangela, kunye neeleyibhile zihanjiswa kwiilwimi zasekuhlaleni ezingama-45 phantsi kwe-`locales/` (ezingama-20 ze-Tier 1, ezili-15 zase-Afrika, nezili-10 zase-Asia).

- I-HTML engaguqukiyo iqala ngesiNgesi kwaye inokwakhiwa nangaluphi na ulwimi lwasekuhlaleni nge-`python3 build.py --lang <locale>`.
- Isihloko esiphezulu sibonelela ngomtshintshi wolwimi oxhaswa yi-`/assets/locales/*.json` onokufumaneka ngokuzenzekelayo kolwimi lwebhrawuza kunye nenkxaso ye-`dir="rtl"` yeelwimi zasekuhlaleni ze-RTL (`ar`, `ar-EG`, `ar-MA`, `fa`, `he`, `ur`).
- Qinisekisa ekuhlaleni nge-`python3 -m unittest discover -s tests`.

## Ukusasaza neLayisensi

I-`.github/workflows/pages.yml` iyakha kwaye isasaze kwi-GitHub Pages kulo lonke u-push kwi-`main` nasemihleni yonke. Jonga i-[README yesiNgesi](../../../README.md) kunye ne-[LICENSE](../../../LICENSE).
