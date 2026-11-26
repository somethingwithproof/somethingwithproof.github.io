> [English](../../../README.md)

# somethingwithproof.github.io

الكود المصدري لموقع https://somethingwithproof.github.io: معرض ثابت للمستودعات العامة مع صفحات توثيق مولّدة تلقائياً.

## البناء

بيتطلب Python 3.12 وأداة GitHub CLI (`gh`)، من غير أي حزم Python خارجية:

```sh
python3 build.py --fetch   # refresh cache/ from GitHub, then build _site/
python3 build.py           # build from cache/
python3 -m http.server -d _site 8765
```

ملف `content/sitemap.json` بيحدد الأقسام والمواضيع والمستودعات. الصفحات المكتوبة يدوياً موجودة في `content/pages/`. صفحات المشاريع بتتولّد من ملفات README الخاصة بالمستودعات بعد تمريرها على منقّي HTML بقائمة سماح (allowlist HTML sanitizer). عملية البناء بتفشل لو أي مستودع في القائمة خاص (private) أو لو نسبة تباين الألوان المولّدة نزلت عن 4.5:1.

## اللغات والترجمة

عناصر واجهة المستخدم والتنقل والبحث والتسميات بتيجي بـ 45 لغة وإعداد محلي تحت `locales/` (20 من الفئة الأولى Tier 1، و15 لغة أفريقية، و10 لغات آسيوية).

- صفحات HTML الثابتة بتبدأ بالإنجليزية كافتراضي، وممكن تتبني بأي لغة عن طريق `python3 build.py --lang <locale>`.
- الشريط العلوي بيوفر مبدّل لغة مدعوم بملفات `/assets/locales/*.json` مع اكتشاف تلقائي للغة المتصفح ودعم `dir="rtl"` للغات اللي بتتكتب من اليمين لليسار (`ar`, `ar-EG`, `ar-MA`, `fa`, `he`, `ur`).
- تحقق محلياً باستخدام `python3 -m unittest discover -s tests`.

## النشر والترخيص

ملف `.github/workflows/pages.yml` بيبني وينشر على GitHub Pages مع كل push على `main` وبشكل يومي. شوف [ملف README الإنجليزي](../../../README.md) الكامل وملف [LICENSE](../../../LICENSE).
