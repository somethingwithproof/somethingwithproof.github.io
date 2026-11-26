> [English](../../../README.md)

# somethingwithproof.github.io

Mã nguồn cho https://somethingwithproof.github.io: thư viện tĩnh trưng bày các kho lưu trữ công khai cùng các trang tài liệu được tạo tự động.

## Xây dựng

Yêu cầu Python 3.12 và GitHub CLI (`gh`), không cần thư viện Python bên thứ ba:

```sh
python3 build.py --fetch   # refresh cache/ from GitHub, then build _site/
python3 build.py           # build from cache/
python3 -m http.server -d _site 8765
```

`content/sitemap.json` định nghĩa các phần, chủ đề và kho lưu trữ. Các trang viết thủ công nằm trong `content/pages/`. Các trang dự án được tạo từ README của kho lưu trữ sau khi đi qua bộ lọc làm sạch HTML theo danh sách cho phép (allowlist). Quá trình dựng sẽ thất bại nếu có bất kỳ kho lưu trữ nào trong danh sách ở trạng thái riêng tư hoặc nếu tỷ lệ tương phản màu được tạo ra giảm xuống dưới 4.5:1.

## Bản địa hóa

Khung giao diện người dùng, điều hướng, tìm kiếm và nhãn được cung cấp sẵn với 45 ngôn ngữ địa phương trong `locales/` (20 ngôn ngữ Bậc 1, 15 ngôn ngữ châu Phi và 10 ngôn ngữ châu Á).

- HTML tĩnh mặc định sử dụng tiếng Anh và có thể được dựng theo bất kỳ ngôn ngữ nào qua `python3 build.py --lang <locale>`.
- Phần đầu trang cung cấp bộ chuyển đổi ngôn ngữ dựa trên `/assets/locales/*.json` kèm tính năng tự động nhận diện ngôn ngữ trình duyệt và hỗ trợ `dir="rtl"` cho các ngôn ngữ RTL (`ar`, `ar-EG`, `ar-MA`, `fa`, `he`, `ur`).
- Kiểm tra cục bộ bằng lệnh `python3 -m unittest discover -s tests`.

## Triển khai và Giấy phép

`.github/workflows/pages.yml` thực hiện dựng và triển khai lên GitHub Pages mỗi khi đẩy mã lên `main` và theo lịch hằng ngày. Xem [README tiếng Anh](../../../README.md) và [LICENSE](../../../LICENSE).
