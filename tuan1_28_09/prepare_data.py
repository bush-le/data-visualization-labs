import os
import pandas as pd

os.makedirs('data', exist_ok=True)

# ==========================================================
# PHẦN 1: DỮ LIỆU DÂN SỐ TP. HỒ CHÍ MINH (MỚI)
# Nguồn: danso.info/dan-so-tp-hcm-moi/
# ==========================================================

# 1. Cơ cấu hợp nhất 3 tỉnh/thành tạo nên TP.HCM mới
sap_nhap_data = [
    {"Component": "TP. Hồ Chí Minh (cũ)", "Population": 9521886, "Area_km2": 2095, "Density_per_km2": 4544, "Share_pct": 70.15},
    {"Component": "Bình Dương (cũ)", "Population": 2858815, "Area_km2": 2695, "Density_per_km2": 1061, "Share_pct": 21.06},
    {"Component": "Bà Rịa - Vũng Tàu (cũ)", "Population": 1192863, "Area_km2": 1983, "Density_per_km2": 602, "Share_pct": 8.79}
]
df_sapnhap = pd.DataFrame(sap_nhap_data)
df_sapnhap.to_csv('data/tphcm_moi_thanh_phan_sap_nhap.csv', index=False, encoding='utf-8-sig')

# 2. Dân số TP.HCM mới qua 10 năm gần đây (2015-2024)
tphcm_10y_data = [
    {"Year": 2015, "Population": 11166100, "National_Share_pct": 12.18, "Area_km2": 6779, "Density_per_km2": 1647, "Growth_Rate_pct": 2.30, "Sex_Ratio": 1.00},
    {"Year": 2016, "Population": 11385300, "National_Share_pct": 12.28, "Area_km2": 6737, "Density_per_km2": 1690, "Growth_Rate_pct": 1.96, "Sex_Ratio": 1.00},
    {"Year": 2017, "Population": 11617200, "National_Share_pct": 12.40, "Area_km2": 6737, "Density_per_km2": 1724, "Growth_Rate_pct": 2.04, "Sex_Ratio": 1.00},
    {"Year": 2018, "Population": 11875200, "National_Share_pct": 12.54, "Area_km2": 6737, "Density_per_km2": 1763, "Growth_Rate_pct": 2.22, "Sex_Ratio": 1.01},
    {"Year": 2019, "Population": 12647100, "National_Share_pct": 13.11, "Area_km2": 6737, "Density_per_km2": 1877, "Growth_Rate_pct": 6.50, "Sex_Ratio": 1.01},
    {"Year": 2020, "Population": 12976090, "National_Share_pct": 13.30, "Area_km2": 6773, "Density_per_km2": 1916, "Growth_Rate_pct": 2.60, "Sex_Ratio": 1.00},
    {"Year": 2021, "Population": 12939710, "National_Share_pct": 13.14, "Area_km2": 6773, "Density_per_km2": 1911, "Growth_Rate_pct": -0.28, "Sex_Ratio": 0.99},
    {"Year": 2022, "Population": 13331540, "National_Share_pct": 13.40, "Area_km2": 6773, "Density_per_km2": 1968, "Growth_Rate_pct": 3.03, "Sex_Ratio": 0.96},
    {"Year": 2023, "Population": 13467600, "National_Share_pct": 13.42, "Area_km2": 6773, "Density_per_km2": 1989, "Growth_Rate_pct": 1.02, "Sex_Ratio": 0.96},
    {"Year": 2024, "Population": 13573564, "National_Share_pct": 13.42, "Area_km2": 6773, "Density_per_km2": 2004, "Growth_Rate_pct": 0.79, "Sex_Ratio": 0.97}
]
df_tphcm_10y = pd.DataFrame(tphcm_10y_data)
df_tphcm_10y.to_csv('data/dan_so_tphcm_moi_10_nam.csv', index=False, encoding='utf-8-sig')

# 3. Cơ cấu dân tộc tại TP.HCM mới
dantoc_data = [
    {"Ethnicity": "Kinh", "Population_TPHCM": 11951874, "Share_TPHCM_pct": 95.11, "National_Pop": 82085826, "Share_National_pct": 14.56},
    {"Ethnicity": "Hoa", "Population_TPHCM": 409549, "Share_TPHCM_pct": 3.26, "National_Pop": 749466, "Share_National_pct": 54.65},
    {"Ethnicity": "Khmer", "Population_TPHCM": 119670, "Share_TPHCM_pct": 0.95, "National_Pop": 1319652, "Share_National_pct": 9.07},
    {"Ethnicity": "Mường", "Population_TPHCM": 13906, "Share_TPHCM_pct": 0.11, "National_Pop": 1452095, "Share_National_pct": 0.96},
    {"Ethnicity": "Chăm", "Population_TPHCM": 13181, "Share_TPHCM_pct": 0.10, "National_Pop": 178948, "Share_National_pct": 7.37},
    {"Ethnicity": "Tày", "Population_TPHCM": 11972, "Share_TPHCM_pct": 0.10, "National_Pop": 1845492, "Share_National_pct": 0.65},
    {"Ethnicity": "Thái", "Population_TPHCM": 10027, "Share_TPHCM_pct": 0.08, "National_Pop": 1820950, "Share_National_pct": 0.55},
    {"Ethnicity": "Nùng", "Population_TPHCM": 9291, "Share_TPHCM_pct": 0.07, "National_Pop": 1083298, "Share_National_pct": 0.86},
    {"Ethnicity": "Chơ Ro", "Population_TPHCM": 8380, "Share_TPHCM_pct": 0.07, "National_Pop": 29520, "Share_National_pct": 28.39},
    {"Ethnicity": "Ê đê", "Population_TPHCM": 4786, "Share_TPHCM_pct": 0.04, "National_Pop": 398671, "Share_National_pct": 1.20},
    {"Ethnicity": "Các dân tộc khác", "Population_TPHCM": 27928, "Share_TPHCM_pct": 0.06, "National_Pop": 0, "Share_National_pct": 0}
]
df_dantoc = pd.DataFrame(dantoc_data)
df_dantoc.to_csv('data/tphcm_moi_co_cau_dan_toc.csv', index=False, encoding='utf-8-sig')

# ==========================================================
# PHẦN 2: BẢNG XẾP HẠNG TOP 10 TỈNH ĐÔNG DÂN NHẤT VIỆT NAM
# THEO DỮ LIỆU MỚI CỦA TP. HỒ CHÍ MINH
# (TP.HCM mới = 13.573.564 người; Bình Dương & BR-VT đã gộp vào TP.HCM)
# ==========================================================

# 4. Top 10 cập nhật theo dữ liệu mới của TP.HCM (Bình Dương đã sáp nhập vào TP.HCM nên An Giang đôn lên Top 10)
top10_new_tphcm = [
    {"Rank": 1, "Province": "TP. Hồ Chí Minh (Mới)", "Region": "Đông Nam Bộ", "Population": 13573564, "Area_km2": 6773, "Density_per_km2": 2004, "Population_Share_pct": 13.42, "Note": "Sáp nhập TP.HCM cũ + Bình Dương + BR-VT"},
    {"Rank": 2, "Province": "Hà Nội", "Region": "Đồng bằng sông Hồng", "Population": 8685607, "Area_km2": 3360, "Density_per_km2": 2585, "Population_Share_pct": 8.59, "Note": "Đô thị đặc biệt"},
    {"Rank": 3, "Province": "Thanh Hóa", "Region": "Bắc Trung Bộ", "Population": 3760650, "Area_km2": 11115, "Density_per_km2": 338, "Population_Share_pct": 3.72, "Note": "Tỉnh đông dân nhất miền Trung"},
    {"Rank": 4, "Province": "Nghệ An", "Region": "Bắc Trung Bộ", "Population": 3470988, "Area_km2": 16486, "Density_per_km2": 211, "Population_Share_pct": 3.43, "Note": "Diện tích lớn nhất Việt Nam"},
    {"Rank": 5, "Province": "Đồng Nai", "Region": "Đông Nam Bộ", "Population": 3341716, "Area_km2": 5864, "Density_per_km2": 570, "Population_Share_pct": 3.30, "Note": "Thủ phủ công nghiệp Đông Nam Bộ"},
    {"Rank": 6, "Province": "Hải Phòng", "Region": "Đồng bằng sông Hồng", "Population": 2121841, "Area_km2": 1527, "Density_per_km2": 1390, "Population_Share_pct": 2.10, "Note": "Đô thị loại đặc biệt / loại 1"},
    {"Rank": 7, "Province": "Hải Dương", "Region": "Đồng bằng sông Hồng", "Population": 1971326, "Area_km2": 1668, "Density_per_km2": 1182, "Population_Share_pct": 1.95, "Note": "Vùng kinh tế trọng điểm Bắc Bộ"},
    {"Rank": 8, "Province": "Bắc Giang", "Region": "Trung du & Miền núi phía Bắc", "Population": 1950615, "Area_km2": 3896, "Density_per_km2": 501, "Population_Share_pct": 1.93, "Note": "Tăng trưởng công nghiệp nhanh"},
    {"Rank": 9, "Province": "Đắk Lắk", "Region": "Tây Nguyên", "Population": 1944821, "Area_km2": 13070, "Density_per_km2": 149, "Population_Share_pct": 1.92, "Note": "Trung tâm vùng Tây Nguyên"},
    {"Rank": 10, "Province": "An Giang", "Region": "Đồng bằng sông Cửu Long", "Population": 1908352, "Area_km2": 3537, "Density_per_km2": 540, "Population_Share_pct": 1.89, "Note": "Đôn lên Top 10 khi Bình Dương vào TP.HCM"}
]
df_top10_new = pd.DataFrame(top10_new_tphcm)
df_top10_new.to_csv('data/top_10_theo_du_lieu_tphcm_moi.csv', index=False, encoding='utf-8-sig')

# 5. Top 10 Tỉnh/Thành đông dân nhất toàn quốc theo phương án sắp xếp sáp nhập 34 tỉnh/thành (Nguồn: danso.info)
top10_34_tinh = [
    {"Rank": 1, "Province": "TP. Hồ Chí Minh (mới)", "Composition": "TP.HCM + Bình Dương + Bà Rịa Vũng Tàu", "Population": 13573564, "Share_pct": 13.42},
    {"Rank": 2, "Province": "Hà Nội", "Composition": "Giữ nguyên địa giới hành chính", "Population": 8685607, "Share_pct": 8.59},
    {"Rank": 3, "Province": "An Giang (mới)", "Composition": "An Giang + Kiên Giang", "Population": 4952238, "Share_pct": 4.90},
    {"Rank": 4, "Province": "Hải Phòng (mới)", "Composition": "Hải Phòng + Hải Dương", "Population": 4664124, "Share_pct": 4.61},
    {"Rank": 5, "Province": "Đồng Nai (mới)", "Composition": "Đồng Nai + Bình Phước", "Population": 4491408, "Share_pct": 4.44},
    {"Rank": 6, "Province": "Ninh Bình (mới)", "Composition": "Ninh Bình + Nam Định + Hà Nam", "Population": 4412264, "Share_pct": 4.36},
    {"Rank": 7, "Province": "Đồng Tháp (mới)", "Composition": "Đồng Tháp + Tiền Giang", "Population": 4370046, "Share_pct": 4.32},
    {"Rank": 8, "Province": "Thanh Hóa", "Composition": "Giữ nguyên địa giới hành chính", "Population": 3760650, "Share_pct": 3.72},
    {"Rank": 9, "Province": "Vĩnh Long (mới)", "Composition": "Vĩnh Long + Trà Vinh + Bến Tre", "Population": 4257581, "Share_pct": 4.21},
    {"Rank": 10, "Province": "Cần Thơ (mới)", "Composition": "Cần Thơ + Hậu Giang + Sóc Trăng", "Population": 4199824, "Share_pct": 4.15}
]
df_top10_34 = pd.DataFrame(top10_34_tinh)
df_top10_34.to_csv('data/top_10_sau_sap_nhap_34_tinh.csv', index=False, encoding='utf-8-sig')

print("Generated all updated datasets successfully!")
