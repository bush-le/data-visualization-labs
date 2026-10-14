# 📊 Trực Quan Hóa Dữ Liệu Dân Số Việt Nam
> **Phần 1: Dữ liệu Dân số TP. Hồ Chí Minh (Mới) | Phần 2: Top 10 Tỉnh Đông Dân Nhất VN theo Dữ Liệu Mới của TP.HCM**

Dự án này thu thập, chuẩn hóa và trực quan hóa dữ liệu từ [danso.info/dan-so-tp-hcm-moi/](https://danso.info/dan-so-tp-hcm-moi/) và dữ liệu xếp hạng từ [danso.info/top-10-tinh-dong-dan-nhat-viet-nam/](https://danso.info/top-10-tinh-dong-dan-nhat-viet-nam/).

---

## 📁 Cấu Trúc Dự Án

```text
data_visualization/
├── dan_so_visualization.ipynb          # Jupyter Notebook hoàn chỉnh (đã pre-render toàn bộ biểu đồ & bảng)
├── data/
│   ├── tphcm_moi_thanh_phan_sap_nhap.csv # Phần 1: Cơ cấu 3 tỉnh/thành sáp nhập tạo nên TP.HCM mới
│   ├── dan_so_tphcm_moi_10_nam.csv     # Phần 1: Dân số TP.HCM mới 10 năm (2015-2024), tốc độ tăng trưởng, mật độ
│   ├── tphcm_moi_co_cau_dan_toc.csv    # Phần 1: Cơ cấu dân tộc tại TP.HCM mới và % so với cả nước
│   ├── top_10_theo_du_lieu_tphcm_moi.csv # Phần 2: Top 10 tỉnh đông dân nhất cập nhật theo quy mô TP.HCM mới
│   └── top_10_sau_sap_nhap_34_tinh.csv  # Phần 2: Bảng xếp hạng Top 10 sau sáp nhập 34 tỉnh toàn quốc
├── images/                             # 9 Biểu đồ xuất bản độ phân giải cao (200 DPI)
│   ├── chart_1.png                     # [P1] Cấu phần sáp nhập tạo nên TP.HCM mới
│   ├── chart_2.png                     # [P1] Diễn biến dân số & mật độ TP.HCM mới (2015-2024)
│   ├── chart_3.png                     # [P1] Tốc độ tăng trưởng hàng năm & phân tích COVID-19
│   ├── chart_4.png                     # [P1] Cơ cấu dân tộc thiểu số và tỷ lệ tập trung tại TP.HCM
│   ├── chart_5.png                     # [P2] Top 10 tỉnh đông dân nhất theo quy mô TP.HCM mới (Thanh ngang)
│   ├── chart_6.png                     # [P2] So sánh TP.HCM Cũ (9.52M) vs TP.HCM Mới (13.57M) trong Top 10
│   ├── chart_7.png                     # [P2] Tỷ trọng dân số Top 10 mới so với toàn quốc (Donut chart)
│   ├── chart_8.png                     # [P2] Bubble chart tương quan Dân số - Diện tích - Mật độ cư trú
│   └── chart_9.png                     # [P2] Bảng xếp hạng Top 10 sau sáp nhập 34 tỉnh toàn quốc
├── prepare_data.py                     # Script tạo lập các bộ dữ liệu CSV
├── create_notebook.py                  # Script xây dựng cấu trúc notebook
└── execute_and_render_notebook.py      # Script thực thi mã và render output vào notebook
```

---

## 📌 Nội Dung Trực Quan Hóa

### 🏙️ Phần 1: Trực Quan Dữ Liệu Dân Số TP. Hồ Chí Minh (Mới)
* **Tổng quy mô siêu đô thị:** **13.573.564 người** (đứng thứ **1/34** đơn vị hành chính sau sáp nhập, chiếm **13,42%** dân số cả nước).
* **Cơ cấu thành phần sáp nhập:** TP.HCM cũ (70,15% - 9,52 triệu), Bình Dương cũ (21,06% - 2,86 triệu), Bà Rịa - Vũng Tàu cũ (8,79% - 1,19 triệu).
* **Diễn biến 10 năm (2015 – 2024):** Tăng từ 11,17 triệu lên 13,57 triệu. Đỉnh tăng trưởng năm 2019 đạt **6,50%** (Tổng điều tra dân số & nhà ở), năm 2021 giảm âm **-0,28%** do tác động đại dịch COVID-19, phục hồi mạnh **+3,03%** vào năm 2022.
* **Cơ cấu dân tộc đặc thù:** Người Kinh chiếm 95,11%. TP.HCM mới là nơi tập trung đến **54,65%** người Hoa và **28,39%** người Chơ Ro của cả nước.

### 🇻🇳 Phần 2: Trực Quan Dữ Liệu Top 10 Tỉnh Đông Dân Nhất VN (Theo Dữ Liệu Mới của TP.HCM)
* **Xếp hạng Top 10 mới:**
  1. **TP. Hồ Chí Minh (Mới):** 13.573.564 người (13,42%)
  2. **Hà Nội:** 8.685.607 người (8,59%)
  3. **Thanh Hóa:** 3.760.650 người (3,72%)
  4. **Nghệ An:** 3.470.988 người (3,43%)
  5. **Đồng Nai:** 3.341.716 người (3,30%)
  6. **Hải Phòng:** 2.121.841 người (2,10%)
  7. **Hải Dương:** 1.971.326 người (1,95%)
  8. **Bắc Giang:** 1.950.615 người (1,93%)
  9. **Đắk Lắk:** 1.944.821 người (1,92%)
  10. **An Giang:** 1.908.352 người (1,89%) *(Đôn lên Top 10 khi Bình Dương hợp nhất vào TP.HCM)*
* **Tỷ trọng Top 10:** Chiếm **43,1%** tổng dân số toàn quốc (~43,6 triệu / ~101,1 triệu dân).
* **Mật độ cư trú sau khi mở rộng:** TP.HCM mới mở rộng diện tích lên 6.773 km², mật độ bình quân điều hòa về **2.004 người/km²**, giảm bớt áp lực so với 4.544 người/km² thời điểm trước sáp nhập; Hà Nội (2.585 người/km²) trở thành địa phương có mật độ cao nhất trong bảng xếp hạng mới.

---

## 💻 Cách Khởi Chạy Notebook

```bash
cd /home/bush/Desktop/data_visualization
jupyter notebook dan_so_visualization.ipynb
```
Hoặc mở trực tiếp file `dan_so_visualization.ipynb` trong VS Code / Antigravity để xem ngay kết quả đã pre-render.
