> [English](../../../README.md)

# somethingwithproof.github.io

https://somethingwithproof.github.io adresi için kaynak kod: otomatik oluşturulan belgelendirme sayfalarına sahip herkese açık depoların statik bir galerisi.

## Derleme

Üçüncü taraf Python bağımlılığı olmadan Python 3.12 ve GitHub CLI (`gh`) gerektirir:

```sh
python3 build.py --fetch   # refresh cache/ from GitHub, then build _site/
python3 build.py           # build from cache/
python3 -m http.server -d _site 8765
```

`content/sitemap.json` bölümleri, konuları ve depoları tanımlar. Elle yazılmış sayfalar `content/pages/` altında bulunur. Proje sayfaları, izin listesi tabanlı bir HTML temizleyiciden (sanitizer) geçirilen depo README dosyalarından üretilir. Listelenen herhangi bir depo özel (private) ise veya üretilen herhangi bir renk kontrast oranı 4.5:1 altına düşerse derleme başarısız olur.

## Yerelleştirme

Arayüz bileşenleri, gezinme, arama ve etiketler `locales/` altında 45 yerel ayarda (20 Tier 1, 15 Afrika ve 10 Asya yerel ayarı) sunulur.

- Statik HTML varsayılan olarak İngilizcedir ve `python3 build.py --lang <locale>` komutuyla herhangi bir yerel ayarda derlenebilir.
- Üst bilgi, `/assets/locales/*.json` tarafından desteklenen bir dil değiştirici, otomatik tarayıcı dili algılama ve RTL yerel ayarları (`ar`, `ar-EG`, `ar-MA`, `fa`, `he`, `ur`) için `dir="rtl"` desteği sunar.
- `python3 -m unittest discover -s tests` komutuyla yerel olarak doğrulayın.

## Dağıtım ve Lisans

`.github/workflows/pages.yml`, `main` dalına her push işleminde ve günlük olarak derleyip GitHub Pages'e dağıtım yapar. [İngilizce README](../../../README.md) ve [LICENSE](../../../LICENSE) dosyalarına bakın.
