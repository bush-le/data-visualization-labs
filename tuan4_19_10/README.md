# 📦 Tuần 4: Trực Quan Hóa Dữ Liệu Logistics & Studio Wedding (19/10/2026)

Thư mục lưu trữ dữ liệu và các nội dung bài tập thực hành tuần 4.

---

## 📁 Cấu trúc thư mục

```text
tuan4_19_10/
├── data/
│   ├── logistics_KHB.csv                 # Dữ liệu vận chuyển/logistics (10.000 dòng, 15 cột)
│   └── studio_wedding_2025.csv           # Dữ liệu khách hàng dịch vụ cưới 2025 (4.748 dòng, 6 cột)
├── description_logistics.md              # Bản thiết kế trực quan hóa chi tiết cho bài toán Logistics (Plotly)
├── description_studio_wedding.md         # Bản thiết kế trực quan hóa chi tiết cho bài toán Studio Cưới (Plotly)
├── build_logistics_notebook.py           # Script tự động tạo & chạy notebook Logistics
├── build_studio_wedding_notebook.py      # Script tự động tạo & chạy notebook Studio Cưới
├── logistics_visualization.ipynb         # Jupyter Notebook hoàn chỉnh có sẵn outputs tương tác Plotly
├── studio_wedding_visualization.ipynb    # Jupyter Notebook hoàn chỉnh có sẵn outputs tương tác Plotly
└── README.md                             # Tài liệu tổng quan Tuần 4
```

---

## 📊 Mô tả các tập dữ liệu

### 1. Dữ liệu Logistics (`logistics_KHB.csv`)
- **Quy mô:** 10.000 bản ghi, 15 trường thông tin.
- **Các trường dữ liệu chính:**
  - `Mã Đơn Hàng`: Mã định danh đơn hàng (VD: `KHB000001`).
  - `Thời Gian`: Thời điểm phát sinh đơn hàng.
  - `Chi Nhánh`: Chi nhánh phụ trách đơn hàng.
  - `Shipper`: Nhân viên giao hàng phụ trách.
  - `Nơi Gửi` / `Nơi Nhận`: Địa điểm giao - nhận hàng (Hà Nội, TP.HCM, Đà Nẵng, v.v.).
  - `Phân Loại`: Hình thức vận chuyển (Nội thành, Liên tỉnh).
  - `Khối Lượng (kg)`: Trọng lượng đơn hàng.
  - `Mặt Hàng`: Nhóm sản phẩm (Điện tử, Thời trang, Thực phẩm khô, v.v.).
  - `Giá Trị (VNĐ)`: Giá trị đơn hàng.
  - `Phí Ship`: Cước phí vận chuyển.
  - `Hình Thức`: Dịch vụ giao hàng (Bình thường, Nhanh).
  - `Thanh Toán`: Hình thức thanh toán (Người gửi/Người nhận thanh toán).
  - `Tình Trạng`: Trạng thái giao hàng (Giao đúng hạn, Giao trễ hạn, v.v.).
  - `Đánh Giá`: Điểm đánh giá dịch vụ (1 - 5 sao).

---

### 2. Dữ liệu Studio Wedding 2025 (`studio_wedding_2025.csv`)
- **Quy mô:** 4.748 bản ghi, 6 trường thông tin.
- **Các trường dữ liệu chính:**
  - `ID_KhachHang`: Mã khách hàng (VD: `KH1000`).
  - `Ngay_Ky_Hop_Dong`: Ngày ký hợp đồng dịch vụ.
  - `Goi_Dich_Vu`: Gói dịch vụ cưới (Studio, Ngoại cảnh, Phim trường, v.v.).
  - `Doanh_Thu`: Giá trị hợp đồng dịch vụ (VNĐ).
  - `Nguon_Khach`: Nguồn tiếp cận khách hàng (Facebook, Người quen, Walk-in, v.v.).
  - `Trang_Thai`: Tiến độ hợp đồng (Đã hoàn thành, Đang thực hiện, v.v.).
