> [English](../../../README.md)

# somethingwithproof.github.io

https://somethingwithproof.github.io کا سورس: تیار کردہ دستاویزاتی صفحات کے ساتھ عوامی ریپوزٹریز کی ایک اسٹیٹک گیلری۔

## بلڈ

بغیر کسی تھرڈ پارٹی Python انحصار کے Python 3.12 اور GitHub CLI (`gh`) درکار ہے:

```sh
python3 build.py --fetch   # refresh cache/ from GitHub, then build _site/
python3 build.py           # build from cache/
python3 -m http.server -d _site 8765
```

`content/sitemap.json` سیکشنز، موضوعات اور ریپوزٹریز کی تعریف کرتی ہے۔ ہاتھ سے لکھے گئے صفحات `content/pages/` میں موجود ہیں۔ پروجیکٹ صفحات ان ریپوزٹری READMEs سے تیار کیے جاتے ہیں جو الاؤ لسٹ HTML سینیٹائزر سے گزرے ہوں۔ اگر فہرست میں شامل کوئی بھی ریپوزٹری پرائیویٹ ہو یا تیار کردہ رنگوں کا کنٹراسٹ تناسب 4.5:1 سے کم ہو جائے تو بلڈ ناکام ہو جاتا ہے۔

## لوکلائزیشن

UI کروم، نیویگیشن، سرچ اور لیبلز `locales/` کے تحت 45 لوکیلز (20 ٹیئر 1، 15 افریقی، اور 10 ایشیائی لوکیلز) میں فراہم کیے جاتے ہیں۔

- اسٹیٹک HTML ڈیفالٹ طور پر انگریزی میں ہوتا ہے اور `python3 build.py --lang <locale>` کے ذریعے کسی بھی لوکیل میں بلڈ کیا جا سکتا ہے۔
- ہیڈر `/assets/locales/*.json` پر مبنی لینگویج سوئچر فراہم کرتا ہے جس میں براؤزر زبان کی خودکار شناخت اور RTL لوکیلز (`ar`، `ar-EG`، `ar-MA`، `fa`، `he`، `ur`) کے لیے `dir="rtl"` سپورٹ شامل ہے۔
- `python3 -m unittest discover -s tests` کے ساتھ مقامی طور پر تصدیق کریں۔

## ڈپلائمنٹ اور لائسنس

`.github/workflows/pages.yml` `main` پر ہر پش کے ساتھ اور روزانہ GitHub Pages پر بلڈ اور ڈپلائی کرتی ہے۔ [انگریزی README](../../../README.md) اور [LICENSE](../../../LICENSE) دیکھیں۔
