> [English](../../../README.md)

# somethingwithproof.github.io

https://somethingwithproof.github.io साठी स्रोत: स्वयंचलितपणे तयार केलेल्या दस्तऐवजीकरण पृष्ठांसह सार्वजनिक रिपॉझिटरीजची स्टॅटिक गॅलरी.

## बिल्ड

कोणत्याही तृतीय-पक्ष Python अवलंबित्वाशिवाय Python 3.12 आणि GitHub CLI (`gh`) आवश्यक आहे:

```sh
python3 build.py --fetch   # refresh cache/ from GitHub, then build _site/
python3 build.py           # build from cache/
python3 -m http.server -d _site 8765
```

`content/sitemap.json` विभाग, विषय आणि रिपॉझिटरीज परिभाषित करते. हस्तलिखित पृष्ठे `content/pages/` मध्ये आहेत. प्रकल्प पृष्ठे अलाउलिस्ट HTML सॅनिटायझरमधून गेलेल्या रिपॉझिटरी READMEs मधून तयार केली जातात. सूचीबद्ध केलेली कोणतीही रिपॉझिटरी खाजगी असल्यास किंवा तयार केलेल्या कोणत्याही रंगाचे कॉन्ट्रास्ट गुणोत्तर 4.5:1 पेक्षा कमी झाल्यास बिल्ड अयशस्वी होते.

## स्थानिकीकरण

UI घटक, नेव्हिगेशन, शोध आणि लेबले `locales/` अंतर्गत 45 लोकॅल्समध्ये उपलब्ध आहेत (20 टियर 1, 15 आफ्रिकन आणि 10 आशियाई लोकॅल्स).

- स्टॅटिक HTML डीफॉल्टनुसार इंग्रजी वापरते आणि `python3 build.py --lang <locale>` द्वारे कोणत्याही लोकॅलमध्ये बिल्ड केले जाऊ शकते.
- हेडरमध्ये `/assets/locales/*.json` द्वारे समर्थित भाषा स्विचर आहे, ज्यामध्ये ब्राउझर भाषा स्वयंचलित ओळख आणि RTL लोकॅल्ससाठी (`ar`, `ar-EG`, `ar-MA`, `fa`, `he`, `ur`) `dir="rtl"` समर्थन आहे.
- `python3 -m unittest discover -s tests` सह स्थानिक पातळीवर पडताळणी करा.

## तैनाती आणि परवाना

`.github/workflows/pages.yml` प्रत्येक `main` पुशवर आणि दररोज GitHub Pages वर बिल्ड आणि तैनात करते. [इंग्रजी README](../../../README.md) आणि [LICENSE](../../../LICENSE) पहा.
