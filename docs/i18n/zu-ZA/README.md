> [English](../../../README.md)

# somethingwithproof.github.io

Umthombo we-https://somethingwithproof.github.io: igalari emi ndawonye yama-repository asesidlangalaleni enamakhasi emibhalo akhiqiziwe.

## Ukwakha

Idinga i-Python 3.12 kanye ne-GitHub CLI (`gh`), ngaphandle kokuncika kwe-Python okuvela eceleni:

```sh
python3 build.py --fetch   # refresh cache/ from GitHub, then build _site/
python3 build.py           # build from cache/
python3 -m http.server -d _site 8765
```

I-`content/sitemap.json` ichaza izigaba, izihloko, kanye nama-repository. Amakhasi abhalwe ngesandla atholakala ku-`content/pages/`. Amakhasi ephrojekthi akhiqizwa kusuka kuma-README ama-repository adluliswe kusihlanzi se-HTML sohlu oluvunyelwe. Ukwakha kuyehluleka uma noma iyiphi i-repository esohlwini iyimfihlo noma uma noma yisiphi isilinganiso sokugqama kombala esikhiqiziwe sehla ngaphansi kuka-4.5:1.

## Ukwenziwa ngokwendawo

I-UI chrome, ukuzulazula, ukusesha, kanye namalebula kulethwa ngezilimi zendawo ezingu-45 ngaphansi kwe-`locales/` (ezingu-20 ze-Tier 1, ezingu-15 zase-Afrika, kanye nezingu-10 zase-Asia).

- I-HTML emi ndawonye isebenzisa isiNgisi ngokuzenzakalelayo futhi ingakhiwa nganoma yiluphi ulimi lwendawo nge-`python3 build.py --lang <locale>`.
- Isihloko sihlinzeka ngesishintshi solimi esisekelwa yi-`/assets/locales/*.json` esinokutholwa kolimi lwesiphequluli ngokuzenzakalelayo kanye nokusekelwa kwe-`dir="rtl"` ezilimini zendawo ze-RTL (`ar`, `ar-EG`, `ar-MA`, `fa`, `he`, `ur`).
- Qinisekisa kukhompyutha yakho nge-`python3 -m unittest discover -s tests`.

## Ukufakwa kanye Nelayisense

I-`.github/workflows/pages.yml` yakha futhi ifake ku-GitHub Pages njalo uma kunokuthunyelwa ku-`main` kanye nansuku zonke. Bheka [i-README yesiNgisi](../../../README.md) kanye ne-[LICENSE](../../../LICENSE).
