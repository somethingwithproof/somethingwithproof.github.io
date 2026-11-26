> [English](../../../README.md)

# somethingwithproof.github.io

የhttps://somethingwithproof.github.io ምንጭ፦ ከተመነጩ የሰነድ ገጾች ጋር የሕዝብ ማከማቻዎች የማይንቀሳቀስ ማዕከለ-ስዕላት።

## ግንባታ

Python 3.12 እና የGitHub CLI (`gh`) ያስፈልገዋል፣ ያለ ምንም የሶስተኛ ወገን Python ጥገኝነቶች፦

```sh
python3 build.py --fetch   # refresh cache/ from GitHub, then build _site/
python3 build.py           # build from cache/
python3 -m http.server -d _site 8765
```

`content/sitemap.json` ክፍሎችን፣ ርዕሶችን እና ማከማቻዎችን ይገልጻል። በእጅ የተጻፉ ገጾች በ`content/pages/` ውስጥ ይገኛሉ። የፕሮጀክት ገጾች በፈቃድ ዝርዝር HTML ማጽጃ ውስጥ ካለፉ የማከማቻ README ፋይሎች ይመነጫሉ። ማንኛውም የተዘረዘረ ማከማቻ የግል ከሆነ ወይም ማንኛውም የተመነጨ የቀለም ንጽጽር ጥምርታ ከ4.5:1 በታች ከወረደ ግንባታው ይከሽፋል።

## አካባቢያዊ ትርጉም

የUI ክፈፍ፣ አሰሳ፣ ፍለጋ እና መለያዎች በ`locales/` ስር በ45 አካባቢዎች (20 ደረጃ 1፣ 15 የአፍሪካ እና 10 የእስያ አካባቢዎች) ይቀርባሉ።

- የማይንቀሳቀስ HTML በነባሪነት እንግሊዝኛ ነው እና በ`python3 build.py --lang <locale>` በኩል በማንኛውም አካባቢ ሊገነባ ይችላል።
- ራስጌው በ`/assets/locales/*.json` የተደገፈ የቋንቋ መቀየሪያ ከራስ-ሰር የአሳሽ ቋንቋ መለየት እና ለRTL አካባቢዎች (`ar`፣ `ar-EG`፣ `ar-MA`፣ `fa`፣ `he`፣ `ur`) የ`dir="rtl"` ድጋፍ ጋር ያቀርባል።
- በአካባቢያዊ ማሽን ላይ በ`python3 -m unittest discover -s tests` ያረጋግጡ።

## ማሰማራት እና ፈቃድ

`.github/workflows/pages.yml` ወደ `main` በሚላክ እያንዳንዱ push እና በየቀኑ ወደ GitHub Pages ይገነባል እንዲሁም ያሰማራል። [የእንግሊዝኛ README](../../../README.md) እና [LICENSE](../../../LICENSE) ይመልከቱ።
