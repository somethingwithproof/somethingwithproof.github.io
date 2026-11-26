> [English](../../../README.md)

# somethingwithproof.github.io

https://somethingwithproof.github.io का स्रोत: जनित दस्तावेज़ीकरण पृष्ठों के साथ सार्वजनिक रिपॉज़िटरी की एक स्थैतिक गैलरी।

## बिल्ड

इसके लिए Python 3.12 और GitHub CLI (`gh`) आवश्यक है, और किसी तृतीय-पक्ष Python निर्भरता की आवश्यकता नहीं है:

```sh
python3 build.py --fetch   # refresh cache/ from GitHub, then build _site/
python3 build.py           # build from cache/
python3 -m http.server -d _site 8765
```

`content/sitemap.json` अनुभागों, विषयों और रिपॉज़िटरी को परिभाषित करता है। हस्तलिखित पृष्ठ `content/pages/` में स्थित हैं। प्रोजेक्ट पृष्ठ उन रिपॉज़िटरी README से जनित होते हैं जिन्हें अनुमति-सूची HTML सैनिटाइज़र से गुजारा जाता है। यदि कोई सूचीबद्ध रिपॉज़िटरी निजी है या कोई जनित रंग कंट्रास्ट अनुपात 4.5:1 से नीचे गिरता है, तो बिल्ड विफल हो जाते हैं।

## स्थानीयकरण

UI क्रोम, नेविगेशन, खोज और लेबल `locales/` के अंतर्गत 45 लोकेल (20 टियर 1, 15 अफ़्रीकी और 10 एशियाई लोकेल) में उपलब्ध हैं।

- स्थैतिक HTML डिफ़ॉल्ट रूप से अंग्रेज़ी में होता है और इसे `python3 build.py --lang <locale>` के माध्यम से किसी भी लोकेल में बनाया जा सकता है।
- हेडर ब्राउज़र भाषा स्वतः-पहचान और RTL लोकेल (`ar`, `ar-EG`, `ar-MA`, `fa`, `he`, `ur`) के लिए `dir="rtl"` समर्थन के साथ `/assets/locales/*.json` द्वारा समर्थित भाषा स्विचर प्रदान करता है।
- `python3 -m unittest discover -s tests` के साथ स्थानीय रूप से सत्यापित करें।

## परिनियोजन और लाइसेंस

`.github/workflows/pages.yml` `main` पर प्रत्येक पुश पर और प्रतिदिन GitHub Pages पर बिल्ड और परिनियोजित करता है। [अंग्रेज़ी README](../../../README.md) और [LICENSE](../../../LICENSE) देखें।
