> [English](../../../README.md)

# somethingwithproof.github.io

Lambar tushe ta https://somethingwithproof.github.io: tarin ma'ajiyoyin jama'a na tsaye tare da shafukan takardun bayani da aka samar.

## Ginawa

Yana buƙatar Python 3.12 da GitHub CLI (`gh`), ba tare da wani dogaro na Python na ɓangare na uku ba:

```sh
python3 build.py --fetch   # refresh cache/ from GitHub, then build _site/
python3 build.py           # build from cache/
python3 -m http.server -d _site 8765
```

`content/sitemap.json` yana ayyana sassa, batutuwa, da ma'ajiyoyi. Shafukan da aka rubuta da hannu suna cikin `content/pages/`. Ana samar da shafukan ayyuka daga fayilolin README na ma'ajiyoyi waɗanda aka tace ta hanyar mai tsabtace HTML mai jerin izini. Ginawa tana gazawa idan wata ma'ajiya da aka jera tana da sirri ko idan bambancin launi da aka samar ya faɗi ƙasa da 4.5:1.

## Daidaita Harshe

Tsarin fuskar amfani, kewayawa, bincike, da alamomi suna zuwa cikin harsuna 45 a ƙarƙashin `locales/` (20 na Mataki na 1, 15 na Afirka, da 10 na Asiya).

- HTML na tsaye yana farawa da Turanci kuma ana iya gina shi a kowane harshe ta hanyar `python3 build.py --lang <locale>`.
- Saman shafin yana da mai sauya harshe wanda `/assets/locales/*.json` ke tallafawa tare da gano harshen burauza ta atomatik da tallafin `dir="rtl"` don harsunan RTL (`ar`, `ar-EG`, `ar-MA`, `fa`, `he`, `ur`).
- Tabbatar a na'urar gida da `python3 -m unittest discover -s tests`.

## Turawa da Lasisi

`.github/workflows/pages.yml` yana ginawa da turawa zuwa GitHub Pages a duk lokacin da aka tura sabon canji zuwa `main` da kuma kowace rana. Duba [README na Turanci](../../../README.md) da [LICENSE](../../../LICENSE).
