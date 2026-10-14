# 🍽️ Tuần 3: Trực Quan Hóa Dữ Liệu Hoạt Động Nhà Hàng (Tháng 11/2025)

Hệ thống biểu đồ được thiết kế theo tiêu chí: **Đơn giản, trực quan, dễ theo dõi, dễ hiểu ngay lập tức** bằng thư viện **Seaborn** & **Matplotlib**. Các số liệu quan trọng đều được ghi chú trực tiếp trên từng thanh/điểm.

---

## 📁 Cấu trúc thư mục

```text
tuan3_12_10/
├── data/
│   └── du_lieu_nha_hang_t11_2025.csv          # Dữ liệu gốc 10.000 giao dịch (UTF-16)
├── images/                                    # 6 biểu đồ trực quan, đơn giản (DPI 300)
│   ├── 01_doanh_thu_theo_thu.png              # Biểu đồ 1: Doanh thu theo từng ngày trong tuần (Cột)
│   ├── 02_luong_khach_theo_khung_gio.png      # Biểu đồ 2: Số lượt bàn theo khung giờ đón khách (Đường)
│   ├── 03_hoa_don_trung_binh_theo_so_khach.png# Biểu đồ 3: Hóa đơn trung bình theo số người trên bàn (Cột)
│   ├── 04_co_cau_thanh_toan_pie.png           # Biểu đồ 4: Tỷ lệ Chuyển khoản vs Tiền mặt (Tròn/Donut)
│   ├── 05_thoi_gian_ngoi_histogram.png        # Biểu đồ 5: Phân bố thời gian ngồi ăn của khách (Histogram)
│   └── 06_co_cau_gioi_tinh.png                # Biểu đồ 6: Tổng số khách Nam vs Nữ (Cột đôi)
├── build_and_execute_notebook.py              # Script tự động tạo & chạy notebook
├── nha_hang_visualization.ipynb               # Jupyter Notebook hoàn chỉnh có sẵn outputs & ảnh
└── README.md                                  # Báo cáo tổng hợp
```

---

## 📊 Danh sách 6 Biểu đồ Trực quan & Đơn giản

| STT | Biểu Đồ | Dạng Biểu Đồ | Ý Nghĩa Trực Quan & Dễ Xem |
| :---: | :--- | :--- | :--- |
| **1** | **Doanh thu theo Thứ** | Cột (`sns.barplot`) | Thấy ngay doanh thu Thứ 7 & CN bùng nổ (>2,6 tỷ/ngày), gấp 2,5 lần ngày thường (~1 tỷ/ngày). |
| **2** | **Lượng khách theo Giờ** | Đường (`sns.lineplot`) | Hiển thị rõ 2 ca cao điểm: Trưa (11h-14h) và Tối (18h-22h), mỗi giờ đón ~1.400 bàn. |
| **3** | **Hóa đơn theo Số khách** | Cột (`sns.barplot`) | Thấy chi tiêu tăng đều theo số người: bàn 1 người (~300k), 4 người (~1,2tr), 8 người (~2,4tr). |
| **4** | **Cơ cấu Thanh toán** | Donut/Tròn | Tỷ lệ cân bằng: Chuyển khoản (50,3%) và Tiền mặt (49,7%). |
| **5** | **Thời gian ngồi ăn** | Tần suất (`sns.histplot`) | Khách ngồi từ 45 - 120 phút, có đường mốc trung bình 82 phút nổi bật. |
| **6** | **Tỷ lệ Giới tính** | Cột đôi (`sns.barplot`) | Thấy ngay số lượng khách Nam (16.828 người) và Nữ (16.779 người) chia đều 50% - 50%. |

---

## 💡 Tóm tắt nhanh cho người xem

1. **Cuối tuần là nguồn thu chính:** Thứ 7 và Chủ Nhật đem lại hơn 5,2 tỷ VNĐ (chiếm hơn một nửa tổng doanh thu cả tuần).
2. **Khung giờ hoạt động:** Nhà hàng nên tập trung nhân sự vào 2 ca cao điểm trưa (11h-14h) và tối (18h-22h).
3. **Mức chi tiêu bình quân:** Khoảng **300.000 VNĐ / khách**.
4. **Vòng quay bàn:** Thời gian ăn trung bình là **82 phút**, khung giờ nhận khách tiếp theo (turnaround time) tối ưu là **90 phút**.
