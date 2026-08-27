# Việt Nam · Độc Lập · Tự Do · Hạnh Phúc

Trang tư liệu về **81 mốc son trong lịch sử dựng nước và giữ nước của dân tộc Việt Nam**,
trình bày theo trục thời gian từ hiện tại lùi về quá khứ, tối ưu cho điện thoại.

Mở `index.html` bằng trình duyệt, hoặc chạy một máy chủ tĩnh trong thư mục này:

```sh
python3 -m http.server 8080
```

## Nội dung

- **81 mốc** chia ba chương: Dựng nước, Giữ nước, Phát triển đất nước.
- **9 mốc trọng điểm** về độc lập và chủ quyền hiển thị dạng thẻ đầy đủ;
  4 trong số đó (938, 1428, 1945, 1975) được nhấn thêm một cấp.
- Mỗi mốc gồm hai lớp: **Ý nghĩa lịch sử** (cô đọng) và **Nội dung lịch sử** (thuật sự kiện).
- Ba bản tuyên ngôn (Nam quốc sơn hà, Bình Ngô đại cáo, Tuyên ngôn Độc lập)
  kèm liên kết toàn văn và video đọc.
- Màu sắc nội suy liên tục theo năm: đồng Đông Sơn → xanh ngọc → lam chàm → son → đỏ Quốc kỳ.

## Cấu trúc

```
index.html          trang đã dựng, mở trực tiếp được
build.sh            dựng lại index.html sau khi sửa nội dung hoặc thêm ảnh
img/                ảnh minh hoạ: img/<số mốc>.<đuôi>, riêng plate.* là tấm Lạc Long Quân – Âu Cơ
_build/
  events.json       81 mốc: ngày, tiêu đề, ý nghĩa lịch sử
  extras.json       nội dung lịch sử từng mốc
  template.src.html giao diện và logic
  baseline.html     khung gốc, không sửa
  assemble.py       script dựng
  fonts/            EB Garamond, Be Vietnam Pro, JetBrains Mono (đã cắt gọn, đủ dấu tiếng Việt)
```

## Sửa nội dung

Sửa `_build/events.json` hoặc `_build/extras.json`, rồi chạy:

```sh
./build.sh
```

Script kiểm tra bắt buộc đủ 81 mốc với id liên tục 1–81; thiếu hoặc trùng sẽ báo lỗi
thay vì dựng ra trang hỏng.

Thêm ảnh: đặt file vào `img/` với tên là **số thứ tự mốc** (ví dụ `img/54.jpg`
cho mốc Tuyên ngôn Độc lập), chấp nhận `.jpg .jpeg .png .webp .avif .gif`, rồi chạy lại `./build.sh`.

## Nguồn

Nội dung biên soạn dựa trên chính sử và tài liệu tham khảo liệt kê ở cuối trang.
Nếu phát hiện sai sót, xin liên hệ để được cập nhật.

Ảnh minh hoạ sưu tầm từ nhiều nguồn, thuộc bản quyền của các tác giả và cơ quan báo chí tương ứng.
