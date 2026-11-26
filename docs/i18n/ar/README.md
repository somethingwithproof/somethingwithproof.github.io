> [English](../../../README.md)

# somethingwithproof.github.io

مصدر الموقع https://somethingwithproof.github.io: معرض ثابت للمستودعات العامة مع صفحات توثيق مُولَّدة.

## البناء

يتطلّب Python 3.12 وأداة سطر أوامر GitHub (`gh`)، دون أي اعتماديات Python خارجية:

```sh
python3 build.py --fetch   # refresh cache/ from GitHub, then build _site/
python3 build.py           # build from cache/
python3 -m http.server -d _site 8765
```

يُعرِّف `content/sitemap.json` الأقسام، والموضوعات، والمستودعات. وتُحفظ الصفحات المكتوبة يدويًا في `content/pages/`. أمّا صفحات المشاريع فتُولَّد من ملفات README للمستودعات بعد تمريرها عبر معقّم HTML قائم على قائمة السماح. ويفشل البناء إذا كان أي مستودع مُدرج خاصًا أو إذا انخفضت نسبة تباين أي لون مُولَّد عن 4.5:1.

## التوطين

تأتي عناصر واجهة المستخدم، والتنقّل، والبحث، والتسميات بـ 45 لغةً وإعدادًا محليًا ضمن `locales/` (20 لغةً من المستوى الأول، و15 لغةً أفريقيةً، و10 لغاتٍ آسيويةٍ).

- تعتمد صفحات HTML الثابتة الإنجليزية افتراضيًا، ويمكن بناؤها بأي لغة عبر `python3 build.py --lang <locale>`.
- توفّر الترويسة مبدّل لغة يعتمد على `/assets/locales/*.json` مع اكتشاف تلقائي للغة المتصفّح ودعم `dir="rtl"` للغات التي تُكتب من اليمين إلى اليسار (`ar`, `ar-EG`, `ar-MA`, `fa`, `he`, `ur`).
- تحقّق محليًا باستخدام `python3 -m unittest discover -s tests`.

## النشر والترخيص

يقوم `.github/workflows/pages.yml` بالبناء والنشر على GitHub Pages عند كل دفع إلى `main` ويوميًا. راجع [ملف README الإنجليزي الكامل](../../../README.md) و[LICENSE](../../../LICENSE).
