> [English](../../../README.md)

# somethingwithproof.github.io

Sumber untuk https://somethingwithproof.github.io: galeri statis repositori publik dengan halaman dokumentasi yang dihasilkan.

## Pembuatan

Memerlukan Python 3.12 dan GitHub CLI (`gh`), tanpa dependensi Python pihak ketiga:

```sh
python3 build.py --fetch   # refresh cache/ from GitHub, then build _site/
python3 build.py           # build from cache/
python3 -m http.server -d _site 8765
```

`content/sitemap.json` mendefinisikan bagian, topik, dan repositori. Halaman tulisan tangan berada di `content/pages/`. Halaman proyek dibuat dari README repositori yang diproses melalui pembersih HTML daftar izin. Proses build akan gagal jika ada repositori terdaftar yang bersifat privat atau jika rasio kontras warna yang dihasilkan turun di bawah 4.5:1.

## Pelokalan

Antarmuka UI, navigasi, pencarian, dan label tersedia dalam 45 lokal di bawah `locales/` (20 lokal Tier 1, 15 lokal Afrika, dan 10 lokal Asia).

- HTML statis menggunakan bahasa Inggris secara bawaan dan dapat dibangun dalam lokal apa pun melalui `python3 build.py --lang <locale>`.
- Header menyediakan pengalih bahasa yang didukung oleh `/assets/locales/*.json` dengan deteksi otomatis bahasa peramban dan dukungan `dir="rtl"` untuk lokal RTL (`ar`, `ar-EG`, `ar-MA`, `fa`, `he`, `ur`).
- Verifikasi secara lokal dengan `python3 -m unittest discover -s tests`.

## Penerapan dan Lisensi

`.github/workflows/pages.yml` membangun dan menerapkan situs ke GitHub Pages pada setiap push ke `main` serta setiap hari. Lihat [README bahasa Inggris](../../../README.md) dan [LICENSE](../../../LICENSE).
