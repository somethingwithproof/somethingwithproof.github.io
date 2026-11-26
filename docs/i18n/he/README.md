> [English](../../../README.md)

# somethingwithproof.github.io

קוד המקור עבור https://somethingwithproof.github.io: גלריה סטטית של מאגרים ציבוריים עם דפי תיעוד המופקים אוטומטית.

## בנייה

דורש Python 3.12 ואת כלי ה-CLI של GitHub (`gh`), ללא תלויות Python של צד שלישי:

```sh
python3 build.py --fetch   # refresh cache/ from GitHub, then build _site/
python3 build.py           # build from cache/
python3 -m http.server -d _site 8765
```

הקובץ `content/sitemap.json` מגדיר מדורים, נושאים ומאגרים. דפים שנכתבו ידנית נמצאים תחת `content/pages/`. דפי פרויקטים מופקים מתוך קובצי README של מאגרים העוברים דרך מנגנון חיטוי HTML המבוסס על רשימת היתר. הבנייה נכשלת אם מאגר כלשהו ברשימה הוא פרטי או אם יחס הניגודיות של צבע שנוצר יורד מתחת ל-4.5:1.

## לוקליזציה

רכיבי מעטפת הממשק, הניווט, החיפוש והתוויות מסופקים ב-45 אזורי שפה תחת `locales/` (20 אזורי Tier 1, 15 אזורים אפריקאיים ו-10 אזורים אסייתיים).

- דפי ה-HTML הסטטיים מוגדרים כברירת מחדל באנגלית וניתן לבנות אותם בכל אזור שפה באמצעות `python3 build.py --lang <locale>`.
- הכותרת העליונה כוללת מחליף שפה המגובה בקובצי `/assets/locales/*.json` עם זיהוי אוטומטי של שפת הדפדפן ותמיכה ב-`dir="rtl"` עבור אזורי שפה הנכתבים מימין לשמאל (`ar`, `ar-EG`, `ar-MA`, `fa`, `he`, `ur`).
- אמתו מקומית באמצעות `python3 -m unittest discover -s tests`.

## פריסה ורישיון

`.github/workflows/pages.yml` בונה ופורס אל GitHub Pages בכל דחיפה אל `main` וכן מדי יום. ראו את קובץ ה-[README המלא באנגלית](../../../README.md) ואת [LICENSE](../../../LICENSE).
