# 📈 Data Visualization Coursework & Exercises

Thư mục lưu trữ và quản lý tập trung toàn bộ các bài tập thực hành, đồ án và trực quan hóa dữ liệu theo từng tuần học.

---

## 📁 Danh Mục Bài Tập Theo Tuần

| Tuần / Ngày | Nội dung chính | Thư mục | Trạng thái |
| :--- | :--- | :--- | :---: |
| **Tuần 1** (28/09/2026) | Trực quan hóa dữ liệu Dân số TP.HCM mới & Top 10 Tỉnh đông dân nhất Việt Nam | [`tuan1_28_09/`](./tuan1_28_09/) | ✅ Hoàn thành |
| **Tuần 2** (05/10/2026) | Trực quan hóa thành tích đoàn Việt Nam tại các kỳ thi Olympic Toán Quốc tế (IMO) | [`tuan2_05_10/`](./tuan2_05_10/) | ✅ Hoàn thành |
| **Tuần 3** (12/10/2026) | Phân tích và trực quan hóa dữ liệu hoạt động nhà hàng (Tháng 11/2025) | [`tuan3_12_10/`](./tuan3_12_10/) | ✅ Hoàn thành |

---

## 📂 Quy Chuẩn Cấu Trúc Thư Mục Cho Các Bài Tập

Mỗi tuần bài tập được tổ chức độc lập trong một thư mục tương ứng: `tuan<SốTuần>_<Ngày>_<Tháng>` (ví dụ: `tuan1_28_09`, `tuan2_05_10`, `tuan3_12_10`):

```text
data_visualization/
├── README.md                          # Mục lục và tổng quan môn học
├── requirements.txt                   # Các thư viện phụ thuộc của dự án
├── tuan1_28_09/                       # Bài tập Tuần 1 (28/09/2026)
│   ├── dan_so_visualization.ipynb    # Jupyter Notebook trực quan hóa dữ liệu
│   ├── data/                         # Tập hợp file CSV / dữ liệu gốc
│   ├── images/                       # Biểu đồ và hình ảnh đã xuất
│   ├── prepare_data.py               # Script chuẩn bị & tiền xử lý dữ liệu
│   └── README.md                     # Báo cáo Tuần 1
├── tuan2_05_10/                       # Bài tập Tuần 2 (05/10/2026)
│   ├── data/                         # Dữ liệu IMO Việt Nam (2015-2024, 2017-2026)
│   ├── charts/                       # Các bộ biểu đồ xuất ra
│   ├── generate_visualizations.py    # Script vẽ biểu đồ
│   └── README.md                     # Báo cáo Tuần 2
└── tuan3_12_10/                       # Bài tập Tuần 3 (12/10/2026)
    ├── data/                         # Dữ liệu hoạt động nhà hàng
    └── README.md                     # Báo cáo Tuần 3
```
