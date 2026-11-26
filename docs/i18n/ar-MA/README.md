> [English](../../../README.md)

# somethingwithproof.github.io

المصدر البرمجي لموقع https://somethingwithproof.github.io: معرض ثابت للمستودعات العامة مع صفحات توثيق مولدة تلقائيا.

## البناء

يتطلب Python 3.12 وأداة GitHub CLI (`gh`)، دون أي تبعيات Python خارجية:

```sh
python3 build.py --fetch   # refresh cache/ from GitHub, then build _site/
python3 build.py           # build from cache/
python3 -m http.server -d _site 8765
```

يحدد `content/sitemap.json` الأقسام والمواضيع والمستودعات. وتوجد الصفحات المكتوبة يدويا في `content/pages/`. يتم توليد صفحات المشاريع من ملفات README الخاصة بالمستودعات بعد تمريرها عبر منقي HTML يعتمد قائمة السماح. تفشل عملية البناء إذا كان أي مستودع مدرج خاصا أو إذا انخفضت نسبة تباين أي لون مولد عن 4.5:1.

## التوطين

تأتي واجهة المستخدم والتنقل والبحث والتسميات بـ 45 لغة محلية ضمن `locales/` (20 من المستوى 1، و15 لغة إفريقية، و10 لغات آسيوية).

- يعتمد HTML الثابت اللغة الإنجليزية افتراضيا ويمكن بناؤه بأي لغة عبر `python3 build.py --lang <locale>`.
- يوفر الشريط العلوي محول لغة يعتمد على `/assets/locales/*.json` مع الكشف التلقائي عن لغة المتصفح ودعم `dir="rtl"` للغات المكتوبة من اليمين إلى اليسار (`ar`، `ar-EG`، `ar-MA`، `fa`، `he`، `ur`).
- تحقق محليا عبر `python3 -m unittest discover -s tests`.

## النشر والترخيص

يبني `.github/workflows/pages.yml` الموقع وينشره على GitHub Pages عند كل دفع إلى `main` وبشكل يومي. راجع [ملف README الإنجليزي الكامل](../../../README.md) و[LICENSE](../../../LICENSE).
