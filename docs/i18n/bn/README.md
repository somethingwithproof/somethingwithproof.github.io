> [English](../../../README.md)

# somethingwithproof.github.io

https://somethingwithproof.github.io সাইটের সোর্স: স্বয়ংক্রিয়ভাবে তৈরি ডকুমেন্টেশন পৃষ্ঠাসহ পাবলিক রিপোজিটরিগুলোর একটি স্ট্যাটিক গ্যালারি।

## বিল্ড

কোনো তৃতীয় পক্ষের Python নির্ভরতা ছাড়াই Python 3.12 এবং GitHub CLI (`gh`) প্রয়োজন:

```sh
python3 build.py --fetch   # refresh cache/ from GitHub, then build _site/
python3 build.py           # build from cache/
python3 -m http.server -d _site 8765
```

`content/sitemap.json` সেকশন, বিষয় এবং রিপোজিটরিগুলো নির্ধারণ করে। হাতে লেখা পৃষ্ঠাগুলো `content/pages/`-এ থাকে। অনুমোদিত তালিকার HTML স্যানিটাইজারের মাধ্যমে পাস করা রিপোজিটরি README থেকে প্রকল্পের পৃষ্ঠাগুলো তৈরি হয়। তালিকাভুক্ত কোনো রিপোজিটরি প্রাইভেট হলে অথবা উৎপন্ন কোনো রঙের কনট্রাস্ট অনুপাত ৪.৫:১-এর নিচে নেমে গেলে বিল্ড ব্যর্থ হয়।

## স্থানীয়করণ

UI ক্রোম, নেভিগেশন, অনুসন্ধান এবং লেবেলগুলো `locales/`-এর অধীনে ৪৫টি লোকেলে (২০টি Tier 1, ১৫টি আফ্রিকান এবং ১০টি এশীয় লোকেল) সরবরাহ করা হয়।

- স্ট্যাটিক HTML ডিফল্টরূপে ইংরেজিতে থাকে এবং `python3 build.py --lang <locale>`-এর মাধ্যমে যেকোনো লোকেলে বিল্ড করা যায়।
- হেডারটিতে `/assets/locales/*.json` দ্বারা সমর্থিত একটি ভাষা পরিবর্তনকারী রয়েছে, যাতে ব্রাউজারের ভাষা স্বয়ংক্রিয় শনাক্তকরণ এবং RTL লোকেলগুলোর (`ar`, `ar-EG`, `ar-MA`, `fa`, `he`, `ur`) জন্য `dir="rtl"` সমর্থন রয়েছে।
- `python3 -m unittest discover -s tests` দিয়ে স্থানীয়ভাবে যাচাই করুন।

## ডিপ্লয় ও লাইসেন্স

`.github/workflows/pages.yml` প্রতিটি `main` পুশে এবং প্রতিদিন GitHub Pages-এ বিল্ড ও ডিপ্লয় করে। [ইংরেজি README](../../../README.md) এবং [LICENSE](../../../LICENSE) দেখুন।
