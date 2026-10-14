# 🏆 Tuần 2: Trực quan hóa Thành tích Đoàn Việt Nam tại IMO (2015 - 2026)

Thư mục chứa mã nguồn, dữ liệu và biểu đồ trực quan hóa kết quả thi Olympic Toán Quốc tế (IMO) của đội tuyển Việt Nam qua 2 giai đoạn: 2015–2024 và 2017–2026.

---

## 📁 Cấu trúc thư mục

```text
tuan2_05_10/
├── data/
│   ├── vietnam_imo_2015_2024.csv    # Dữ liệu IMO giai đoạn 2015 - 2024
│   └── vietnam_imo_2017_2026.csv    # Dữ liệu IMO giai đoạn 2017 - 2026
├── charts/
│   ├── period_2015_2024/            # Bộ 6 biểu đồ phân tích giai đoạn 2015 - 2024
│   └── period_2017_2026/            # Bộ 6 biểu đồ phân tích giai đoạn 2017 - 2026
├── generate_visualizations.py       # Script sinh các biểu đồ trực quan hóa
└── README.md
```

## 📊 Danh mục biểu đồ đã trực quan hóa
1. **01_co_cau_huy_chuong.png**: Biểu đồ cột chồng thể hiện cơ cấu giải thưởng từng năm (Vàng, Bạc, Đồng, Bằng khen).
2. **02_thu_hang_va_tong_diem.png**: Biểu đồ kết hợp 2 trục tung (Dual-axis) theo dõi xu hướng Tổng điểm và Thứ hạng toàn đoàn.
3. **03_tong_co_cau_giai_thuong.png**: Biểu đồ tròn thể hiện tỉ lệ phần trăm các loại huy chương đạt được qua 10 năm.
4. **04_diem_trung_binh_thi_sinh.png**: Biểu đồ diện tích / đường thể hiện điểm trung bình mỗi thí sinh so sánh với mốc chuẩn.
5. **05_tan_suat_xep_hang_toan_doan.png**: Biểu đồ phân phối tần suất nhóm thứ hạng của đoàn Việt Nam.
6. **06_tuong_quan_diem_va_thu_hang.png**: Biểu đồ phân tán & hồi quy tuyến tính thể hiện tương quan giữa Tổng điểm và Thứ hạng.
