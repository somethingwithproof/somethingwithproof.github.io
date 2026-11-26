> [English](../../../README.md)

# somethingwithproof.github.io

Sumber untuk https://somethingwithproof.github.io: galeri statik repositori awam dengan halaman dokumentasi yang dijana.

## Binaan

Memerlukan Python 3.12 dan GitHub CLI (`gh`), tanpa kebergantungan Python pihak ketiga:

```sh
python3 build.py --fetch   # refresh cache/ from GitHub, then build _site/
python3 build.py           # build from cache/
python3 -m http.server -d _site 8765
```

`content/sitemap.json` mentakrifkan bahagian, topik, dan repositori. Halaman yang ditulis tangan terletak dalam `content/pages/`. Halaman projek dijana daripada README repositori yang dilalukan melalui pembersih HTML senarai dibenarkan. Binaan gagal jika mana-mana repositori tersenarai adalah peribadi atau jika sebarang nisbah kontras warna yang dijana turun di bawah 4.5:1.

## Penyetempatan

Elemen antara muka pengguna, navigasi, carian, dan label dibekalkan dalam 45 lokal di bawah `locales/` (20 lokal Peringkat 1, 15 lokal Afrika, dan 10 lokal Asia).

- HTML statik lalai kepada Bahasa Inggeris dan boleh dibina dalam sebarang lokal melalui `python3 build.py --lang <locale>`.
- Pengepala menyediakan penukar bahasa yang disokong oleh `/assets/locales/*.json` dengan pengesanan automatik bahasa pelayar dan sokongan `dir="rtl"` untuk lokal RTL (`ar`, `ar-EG`, `ar-MA`, `fa`, `he`, `ur`).
- Sahkan secara setempat dengan `python3 -m unittest discover -s tests`.

## Pengerahan dan Lesen

`.github/workflows/pages.yml` membina dan mengerahkan ke GitHub Pages pada setiap tolakan ke `main` dan secara harian. Lihat [README Bahasa Inggeris](../../../README.md) dan [LICENSE](../../../LICENSE).
