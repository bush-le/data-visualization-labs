import os
import sys
import json
import io
import contextlib
import pandas as pd
import numpy as np
import nbformat as nbf
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "studio_wedding_2025.csv")
NB_PATH = os.path.join(BASE_DIR, "studio_wedding_visualization.ipynb")

print("Đang khởi tạo cấu trúc Notebook Studio Wedding...")

cells = []

def add_md(text):
    cells.append(nbf.v4.new_markdown_cell(text.strip()))

def add_code(code):
    cells.append(nbf.v4.new_code_cell(code.strip()))

# ==============================================================================
# 1. TIÊU ĐỀ BÁO CÁO
# ==============================================================================
add_md("""# 💍 Báo Cáo Trực Quan Hóa Tương Tác Dữ Liệu Studio Cưới 2025
## 📌 Phân Tích Hiệu Quả Kinh Doanh, Chu Kỳ Mùa Vụ & Kênh Tiếp Thị Số Bằng Thư Viện Plotly

---

### 🎯 Mục tiêu dự án
Báo cáo phân tích toàn diện hoạt động kinh doanh của **Studio Ảnh Cưới** trong năm 2025 dựa trên 4.748 hợp đồng ký kết. Hệ thống biểu đồ tương tác Plotly được thiết kế theo phong cách **Đơn giản – Tinh tế – Trực quan – Đi từ Tổng quan đến Chi tiết**, giúp người xem hiểu thấu đáo cấu trúc nguồn thu và hành vi khách hàng.

### 🧭 Lộ trình phân tích 4 tầng:
1. **Tầng 1: Tổng quan Doanh thu & Chỉ số Kinh doanh Cốt lõi** – Bộ 4 thẻ KPI tài chính và biểu đồ Donut kép so sánh tương phản Số lượng khách vs Tỷ trọng doanh thu (Quy luật Pareto).
2. **Tầng 2: Tính Mùa vụ Cưới & Xu hướng Tăng trưởng 2025** – Biểu đồ 12 tháng nhận diện 2 đỉnh mùa cưới và đáy "Tháng Ngâu", kèm đường tích lũy doanh thu 365 ngày với Date Range Slider.
3. **Tầng 3: Hiệu quả Kênh Tiếp thị & Chuyển đổi Khách hàng** – Đánh giá đóng góp của Facebook, TikTok, Người quen, Walk-in và phân tích sở thích chọn gói dịch vụ của từng kênh.
4. **Tầng 4: Quản trị Tiến độ Hợp đồng & Dòng chảy Giá trị** – Kiểm soát tiến độ giao sản phẩm theo tháng và sơ đồ dòng chảy Sankey toàn cảnh: *Nguồn Khách ➔ Gói Dịch Vụ ➔ Trạng Thái Hợp Đồng*.
""")

# ==============================================================================
# 2. KHỞI TẠO MÔI TRƯỜNG & TIỀN XỬ LÝ DỮ LIỆU
# ==============================================================================
add_code("""# 1. Khai báo thư viện và cấu hình phong cách hiển thị Plotly
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

# Thiết lập template giao diện
pio.renderers.default = "notebook_connected"
PLOTLY_TEMPLATE = "plotly_white"

# Bảng màu thương hiệu cưới sang trọng, trang nhã
WEDDING_PALETTE = {
    "Ngoại cảnh": "#D4AF37",    # Vàng kim (Warm Gold - Cao cấp nhất)
    "Phim trường": "#E0A96D",   # Hồng đất / Rose Gold (Phân khúc tầm trung)
    "Studio": "#5DADE2",        # Xanh dương pastel (Gói cơ bản)
    "Đã hoàn thành": "#27AE60", # Xanh lục ngọc (Hoàn tất)
    "Đang thực hiện": "#E67E22" # Cam hổ phách (Đang phục vụ)
}

# 2. Đọc và tiền xử lý dữ liệu hợp đồng cưới
df = pd.read_csv("data/studio_wedding_2025.csv")

# Xử lý thời gian và quy đổi đơn vị tài chính
df["Ngay_Ky_Hop_Dong"] = pd.to_datetime(df["Ngay_Ky_Hop_Dong"])
df["Tháng"] = df["Ngay_Ky_Hop_Dong"].dt.month
df["Quý"] = "Q" + df["Ngay_Ky_Hop_Dong"].dt.quarter.astype(str)
df["Doanh_Thu_Ty"] = df["Doanh_Thu"] / 1e9        # Đơn vị: Tỷ VNĐ
df["Doanh_Thu_Trieu"] = df["Doanh_Thu"] / 1e6     # Đơn vị: Triệu VNĐ

print(f"✅ Đã tải thành công: {len(df):,} hợp đồng cưới năm 2025.")
print(f"💰 Tổng doanh thu: {df['Doanh_Thu'].sum():,} VNĐ (~{df['Doanh_Thu_Ty'].sum():.2f} Tỷ VNĐ).")
print(f"📅 Khoảng thời gian: Từ {df['Ngay_Ky_Hop_Dong'].min().strftime('%d/%m/%Y')} đến {df['Ngay_Ky_Hop_Dong'].max().strftime('%d/%m/%Y')}.")
df.head(3)""")

# ==============================================================================
# 3. TẦNG 1: TỔNG QUAN DOANH THU & CHỈ SỐ KINH DOANH CỐT LÕI
# ==============================================================================
add_md("""---
## 📊 Tầng 1: Tổng Quan Doanh Thu & Chỉ Số Kinh Doanh Cốt Lõi (Strategic Overview)

Tầng phân tích khởi đầu giúp Ban Điều hành nắm vững các con số tài chính cốt lõi và phát hiện sự phân hóa tỷ trọng doanh thu giữa các gói dịch vụ cưới.
""")

add_code("""# Biểu đồ 1.1: Bảng Thẻ Chỉ Số Kinh Doanh Doanh Nghiệp (Executive KPI Board)
total_revenue_ty = df["Doanh_Thu_Ty"].sum()
total_contracts = len(df)
aov_trieu = df["Doanh_Thu_Trieu"].mean()
completed_count = (df["Trang_Thai"] == "Đã hoàn thành").sum()
completion_rate = completed_count / total_contracts * 100

fig1_1 = go.Figure()

fig1_1.add_trace(go.Indicator(
    mode="number",
    value=total_revenue_ty,
    number={"suffix": " Tỷ", "valueformat": ".2f", "font": {"size": 38, "color": "#D4AF37"}},
    title={"text": "<b>TỔNG DOANH THU 2025</b><br><span style='font-size:12px;color:gray'>44.91 Tỷ VNĐ</span>"},
    domain={"row": 0, "column": 0}
))

fig1_1.add_trace(go.Indicator(
    mode="number",
    value=total_contracts,
    number={"valueformat": ",d", "font": {"size": 38, "color": "#2C3E50"}},
    title={"text": "<b>TỔNG SỐ HỢP ĐỒNG</b><br><span style='font-size:12px;color:gray'>4,748 cặp đôi ký kết</span>"},
    domain={"row": 0, "column": 1}
))

fig1_1.add_trace(go.Indicator(
    mode="number",
    value=aov_trieu,
    number={"suffix": " Tr", "valueformat": ".2f", "font": {"size": 38, "color": "#8E44AD"}},
    title={"text": "<b>GIÁ TRỊ TB / HỢP ĐỒNG (AOV)</b><br><span style='font-size:12px;color:gray'>9.46 Triệu VNĐ / khách</span>"},
    domain={"row": 0, "column": 2}
))

fig1_1.add_trace(go.Indicator(
    mode="number",
    value=completion_rate,
    number={"suffix": "%", "valueformat": ".1f", "font": {"size": 38, "color": "#27AE60"}},
    title={"text": "<b>TỶ LỆ HOÀN THÀNH</b><br><span style='font-size:12px;color:gray'>4,240 hợp đồng xong trọn gói</span>"},
    domain={"row": 0, "column": 3}
))

fig1_1.update_layout(
    grid={"rows": 1, "columns": 4, "pattern": "independent"},
    template=PLOTLY_TEMPLATE,
    height=220,
    margin=dict(l=20, r=20, t=50, b=20),
    title="<b>BẢNG ĐIỀU KHIỂN CHỈ SỐ KINH DOANH STUDIO CƯỚI 2025 (EXECUTIVE KPI BOARD)</b>",
    title_x=0.5
)
fig1_1.show()""")

add_code("""# Biểu đồ 1.2: So Sánh Tương Phản: Cơ Cấu Lượng Khách vs Tỷ Trọng Doanh Thu (Donut Kép)
pkg_summary = df.groupby("Goi_Dich_Vu").agg(
    So_Khach=("ID_KhachHang", "count"),
    Doanh_Thu_Ty=("Doanh_Thu_Ty", "sum")
).reset_index()

# Đảm bảo thứ tự hiển thị: Studio, Phim trường, Ngoại cảnh
pkg_order = ["Studio", "Phim trường", "Ngoại cảnh"]
pkg_summary["Goi_Dich_Vu"] = pd.Categorical(pkg_summary["Goi_Dich_Vu"], categories=pkg_order, ordered=True)
pkg_summary = pkg_summary.sort_values("Goi_Dich_Vu")

fig1_2 = make_subplots(
    rows=1, cols=2,
    specs=[[{"type": "domain"}, {"type": "domain"}]],
    subplot_titles=["<b>1. Cơ Cấu Số Lượng Khách Hàng (%)</b>", "<b>2. Tỷ Trọng Doanh Thu Đóng Góp (%)</b>"]
)

# Donut 1: Số lượng khách
fig1_2.add_trace(
    go.Pie(
        labels=pkg_summary["Goi_Dich_Vu"],
        values=pkg_summary["So_Khach"],
        hole=0.55,
        marker=dict(colors=[WEDDING_PALETTE[p] for p in pkg_summary["Goi_Dich_Vu"]]),
        textinfo="label+percent",
        hovertemplate="Gói: <b>%{label}</b><br>Khách hàng: <b>%{value:,} người</b><br>Tỷ lệ: <b>%{percent:.1%}</b><extra></extra>"
    ),
    row=1, col=1
)

# Donut 2: Doanh thu
fig1_2.add_trace(
    go.Pie(
        labels=pkg_summary["Goi_Dich_Vu"],
        values=pkg_summary["Doanh_Thu_Ty"],
        hole=0.55,
        marker=dict(colors=[WEDDING_PALETTE[p] for p in pkg_summary["Goi_Dich_Vu"]]),
        textinfo="label+percent",
        hovertemplate="Gói: <b>%{label}</b><br>Doanh thu: <b>%{value:.2f} Tỷ VNĐ</b><br>Tỷ trọng: <b>%{percent:.1%}</b><extra></extra>"
    ),
    row=1, col=2
)

fig1_2.update_layout(
    title="<b>Nghịch Lý Phân Hóa Giá Trị: Cơ Cấu Số Khách Hàng vs Tỷ Trọng Doanh Thu</b>",
    title_x=0.5,
    template=PLOTLY_TEMPLATE,
    height=480,
    legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
)
fig1_2.show()""")

# ==============================================================================
# 4. TẦNG 2: TÍNH MÙA VỤ CƯỚI & XU HƯỚNG TĂNG TRƯỞNG NĂM 2025
# ==============================================================================
add_md("""---
## 📈 Tầng 2: Tính Mùa Vụ Cưới & Xu Hướng Tăng Trưởng Năm 2025 (Seasonality Trends)

Thị trường cưới hỏi tại Việt Nam chịu sự chi phối mạnh mẽ của yếu tố văn hóa truyền thống, thời tiết và âm lịch. Biểu đồ dưới đây khắc họa rõ nét các đợt sóng cao điểm và khoảng trũng trong năm.
""")

add_code("""# Biểu đồ 2.1: Diễn Biến Doanh Thu & Lượng Hợp Đồng Cưới 12 Tháng Năm 2025
monthly_stat = df.groupby("Tháng").agg(
    Doanh_Thu_Ty=("Doanh_Thu_Ty", "sum"),
    So_Hop_Dong=("ID_KhachHang", "count")
).reset_index()

fig2_1 = make_subplots(specs=[[{"secondary_y": True}]])

# 1. Cột doanh thu hàng tháng
fig2_1.add_trace(
    go.Bar(
        x=monthly_stat["Tháng"],
        y=monthly_stat["Doanh_Thu_Ty"],
        name="Doanh thu (Tỷ VNĐ)",
        marker_color="#D4AF37",
        hovertemplate="Tháng %{x}: <b>%{y:.2f} Tỷ VNĐ</b><extra></extra>"
    ),
    secondary_y=False
)

# 2. Đường số lượng hợp đồng ký mới
fig2_1.add_trace(
    go.Scatter(
        x=monthly_stat["Tháng"],
        y=monthly_stat["So_Hop_Dong"],
        name="Số lượng hợp đồng",
        mode="lines+markers+text",
        line=dict(color="#2C3E50", width=3),
        marker=dict(size=8, color="#1A252F"),
        text=[f"{v:,}" for v in monthly_stat["So_Hop_Dong"]],
        textposition="top center",
        hovertemplate="Số hợp đồng: <b>%{y:,} HĐ</b><extra></extra>"
    ),
    secondary_y=True
)

# Ghi chú các mốc đặc biệt
fig2_1.add_annotation(
    x=12, y=7.65, xref="x", yref="y",
    text="<b>ĐỈNH MÙA CƯỚI CUỐI NĂM</b><br>Tháng 12: 7.65 Tỷ (785 HĐ)",
    showarrow=True, arrowhead=2, arrowcolor="#C0392B", ax=-80, ay=-40,
    bgcolor="rgba(255, 235, 238, 0.9)", bordercolor="#E74C3C"
)

fig2_1.add_annotation(
    x=1, y=7.41, xref="x", yref="y",
    text="<b>ĐỈNH CƯỚI ĐÓN TẾT</b><br>Tháng 1: 7.41 Tỷ (747 HĐ)",
    showarrow=True, arrowhead=2, arrowcolor="#C0392B", ax=70, ay=-40,
    bgcolor="rgba(255, 235, 238, 0.9)", bordercolor="#E74C3C"
)

fig2_1.add_annotation(
    x=8, y=1.38, xref="x", yref="y",
    text="<b>ĐÁY THÁNG NGÂU (T7 Âm lịch)</b><br>Tháng 8: Chỉ 1.38 Tỷ (150 HĐ)",
    showarrow=True, arrowhead=2, arrowcolor="#2980B9", ax=0, ay=-45,
    bgcolor="rgba(235, 245, 255, 0.9)", bordercolor="#3498DB"
)

fig2_1.update_layout(
    title="<b>Diễn Biến Doanh Thu & Số Hợp Đồng 12 Tháng Năm 2025 (Chu Kỳ Mùa Vụ Cưới)</b>",
    title_x=0.5,
    xaxis=dict(title="Tháng ký hợp đồng", tickmode="linear", tick0=1, dtick=1),
    yaxis=dict(title="Doanh thu (Tỷ VNĐ)", range=[0, 9], showgrid=True),
    yaxis2=dict(title="Số lượng hợp đồng (Hợp đồng)", range=[0, 950], showgrid=False),
    template=PLOTLY_TEMPLATE,
    height=550,
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.03, xanchor="center", x=0.5)
)
fig2_1.show()""")

add_code("""# Biểu đồ 2.2: Doanh Thu Tích Lũy 365 Ngày Năm 2025 (Cumulative Area Chart)
daily_revenue = df.groupby("Ngay_Ky_Hop_Dong")["Doanh_Thu_Ty"].sum().reset_index()
daily_revenue = daily_revenue.sort_values("Ngay_Ky_Hop_Dong")
daily_revenue["Luy_Ke_Ty"] = daily_revenue["Doanh_Thu_Ty"].cumsum()

fig2_2 = px.area(
    daily_revenue,
    x="Ngay_Ky_Hop_Dong",
    y="Luy_Ke_Ty",
    title="<b>Tốc Độ Tăng Trưởng Doanh Thu Tích Lũy 365 Ngày Năm 2025</b>",
    labels={"Ngay_Ky_Hop_Dong": "Ngày ký hợp đồng", "Luy_Ke_Ty": "Doanh thu tích lũy (Tỷ VNĐ)"},
    template=PLOTLY_TEMPLATE
)

fig2_2.update_traces(
    line=dict(color="#D4AF37", width=2.5),
    fillcolor="rgba(212, 175, 55, 0.25)",
    hovertemplate="Ngày: <b>%{x|%d/%m/%Y}</b><br>Doanh thu tích lũy: <b>%{y:.2f} Tỷ VNĐ</b><extra></extra>"
)

fig2_2.update_layout(
    title_x=0.5,
    height=480,
    xaxis=dict(
        title="Dòng thời gian năm 2025",
        rangeslider=dict(visible=True)  # Thanh trượt thời gian tương tác
    ),
    yaxis=dict(title="Doanh thu tích lũy (Tỷ VNĐ)")
)
fig2_2.show()""")

# ==============================================================================
# 5. TẦNG 3: HIỆU QUẢ KÊNH TIẾP THỊ & CHUYỂN ĐỔI KHÁCH HÀNG
# ==============================================================================
add_md("""---
## 🎯 Tầng 3: Hiệu Quả Kênh Tiếp Thị & Chuyển Đổi Khách Hàng (Marketing Attribution)

Đánh giá chính xác kênh tiếp thị nào mang lại doanh thu cao nhất và phân tích xu hướng chi tiêu của khách hàng theo từng nguồn chuyển đổi.
""")

add_code("""# Biểu đồ 3.1: Xếp Hạng Doanh Thu & Khách Hàng Theo 4 Kênh Thu Hút (Horizontal Bar)
channel_stat = df.groupby("Nguon_Khach").agg(
    Doanh_Thu_Ty=("Doanh_Thu_Ty", "sum"),
    So_Khach=("ID_KhachHang", "count")
).reset_index().sort_values("Doanh_Thu_Ty", ascending=True)

fig3_1 = go.Figure()

fig3_1.add_trace(go.Bar(
    y=channel_stat["Nguon_Khach"],
    x=channel_stat["Doanh_Thu_Ty"],
    orientation="h",
    marker_color=["#95A5A6", "#2ECC71", "#111111", "#1877F2"],  # Walk-in, Người quen, TikTok, Facebook
    text=[f"<b>{rev:.2f} Tỷ</b> ({cnt:,} khách)" for rev, cnt in zip(channel_stat["Doanh_Thu_Ty"], channel_stat["So_Khach"])],
    textposition="outside",
    hovertemplate="Kênh: <b>%{y}</b><br>Doanh thu: <b>%{x:.2f} Tỷ VNĐ</b><extra></extra>"
))

fig3_1.update_layout(
    title="<b>Xếp Hạng Doanh Thu & Lượng Khách Hàng Theo 4 Kênh Tiếp Cận</b>",
    title_x=0.5,
    xaxis=dict(title="Doanh thu đóng góp (Tỷ VNĐ)", range=[0, 21]),
    yaxis=dict(title="Kênh tiếp thị"),
    template=PLOTLY_TEMPLATE,
    height=420
)
fig3_1.show()""")

add_code("""# Biểu đồ 3.2: Cơ Cấu Gói Dịch Vụ Theo Từng Kênh Tiếp Cận (100% Normalized Bar)
channel_pkg = pd.crosstab(df["Nguon_Khach"], df["Goi_Dich_Vu"], normalize="index") * 100
channel_pkg = channel_pkg[pkg_order]  # Đảm bảo thứ tự gói

fig3_2 = go.Figure()

for pkg in pkg_order:
    fig3_2.add_trace(go.Bar(
        x=channel_pkg.index,
        y=channel_pkg[pkg],
        name=pkg,
        marker_color=WEDDING_PALETTE[pkg],
        text=[f"{v:.1f}%" for v in channel_pkg[pkg]],
        textposition="inside",
        insidetextanchor="middle",
        hovertemplate="Kênh: <b>%{x}</b><br>Gói dịch vụ: <b>" + pkg + "</b><br>Tỷ lệ: <b>%{y:.2f}%</b><extra></extra>"
    ))

fig3_2.update_layout(
    barmode="stack",
    title="<b>Tỷ Lệ Lựa Chọn Gói Dịch Vụ Theo Từng Kênh Khách Hàng (Normalized 100%)</b>",
    title_x=0.5,
    xaxis=dict(title="Kênh tiếp cận"),
    yaxis=dict(title="Tỷ lệ cơ cấu gói (%)", range=[0, 100]),
    template=PLOTLY_TEMPLATE,
    height=480,
    legend=dict(orientation="h", yanchor="bottom", y=1.03, xanchor="center", x=0.5)
)
fig3_2.show()""")

# ==============================================================================
# 6. TẦNG 4: QUẢN TRỊ TIẾN ĐỘ HỢP ĐỒNG & DÒNG CHẢY GIÁ TRỊ
# ==============================================================================
add_md("""---
## 🔄 Tầng 4: Quản Trị Tiến Độ Hợp Đồng & Dòng Chảy Giá Trị (Fulfillment & Flow)

Đảm bảo tiến độ hoàn thành cam kết với khách hàng và trực quan hóa trọn vẹn dòng chảy từ Kênh thu hút ➔ Gói dịch vụ ➔ Trạng thái xử lý.
""")

add_code("""# Biểu đồ 4.1: Tiến Độ Hợp Đồng Cưới Theo Tháng Ký Kết (Stacked Bar)
monthly_status = pd.crosstab(df["Tháng"], df["Trang_Thai"])

fig4_1 = go.Figure()

for status in ["Đã hoàn thành", "Đang thực hiện"]:
    fig4_1.add_trace(go.Bar(
        x=monthly_status.index,
        y=monthly_status[status],
        name=status,
        marker_color=WEDDING_PALETTE[status],
        text=[f"{v:,}" if v > 0 else "" for v in monthly_status[status]],
        textposition="inside",
        insidetextanchor="middle",
        hovertemplate="Tháng: <b>%{x}</b><br>Trạng thái: <b>" + status + "</b><br>Số lượng: <b>%{y:,} HĐ</b><extra></extra>"
    ))

fig4_1.update_layout(
    barmode="stack",
    title="<b>Tiến Độ Thực Hiện Hợp Đồng Cưới Theo Từng Tháng Trong Năm 2025</b>",
    title_x=0.5,
    xaxis=dict(title="Tháng ký hợp đồng", tickmode="linear", tick0=1, dtick=1),
    yaxis=dict(title="Số lượng hợp đồng (HĐ)"),
    template=PLOTLY_TEMPLATE,
    height=480,
    legend=dict(orientation="h", yanchor="bottom", y=1.03, xanchor="center", x=0.5)
)
fig4_1.show()""")

add_code("""# Biểu đồ 4.2: Sơ Đồ Dòng Chảy Giá Trị Toàn Diện (Sankey Flow Diagram)
# Luồng 1: Kênh Tiếp Thị -> Gói Dịch Vụ
flow1 = df.groupby(["Nguon_Khach", "Goi_Dich_Vu"])["Doanh_Thu_Ty"].sum().reset_index()
# Luồng 2: Gói Dịch Vụ -> Trạng Thái
flow2 = df.groupby(["Goi_Dich_Vu", "Trang_Thai"])["Doanh_Thu_Ty"].sum().reset_index()

sources = list(df["Nguon_Khach"].unique())
packages = pkg_order
statuses = ["Đã hoàn thành", "Đang thực hiện"]

all_nodes = sources + packages + statuses
node_colors = ["#1877F2", "#95A5A6", "#2ECC71", "#111111"] + [WEDDING_PALETTE[p] for p in packages] + [WEDDING_PALETTE[s] for s in statuses]

src_list = []
tgt_list = []
val_list = []

# Nối Kênh -> Gói
for _, row in flow1.iterrows():
    src_list.append(all_nodes.index(row["Nguon_Khach"]))
    tgt_list.append(all_nodes.index(row["Goi_Dich_Vu"]))
    val_list.append(row["Doanh_Thu_Ty"])

# Nối Gói -> Trạng Thái
for _, row in flow2.iterrows():
    src_list.append(all_nodes.index(row["Goi_Dich_Vu"]))
    tgt_list.append(all_nodes.index(row["Trang_Thai"]))
    val_list.append(row["Doanh_Thu_Ty"])

fig4_2 = go.Figure(data=[go.Sankey(
    node=dict(
        pad=20,
        thickness=25,
        line=dict(color="black", width=0.5),
        label=all_nodes,
        color=node_colors
    ),
    link=dict(
        source=src_list,
        target=tgt_list,
        value=val_list,
        color="rgba(212, 175, 55, 0.35)",
        hovertemplate="Chuyển dịch: <b>%{source.label} ➔ %{target.label}</b><br>Doanh thu: <b>%{value:.2f} Tỷ VNĐ</b><extra></extra>"
    )
)])

fig4_2.update_layout(
    title="<b>Sơ Đồ Dòng Chảy Chuyển Đổi Giá Trị (Kênh Tiếp Thị ➔ Gói Dịch Vụ ➔ Trạng Thái)</b>",
    title_x=0.5,
    font=dict(family="Arial", size=13),
    template=PLOTLY_TEMPLATE,
    height=550,
    margin=dict(t=70, l=20, r=20, b=20)
)
fig4_2.show()""")

# ==============================================================================
# 7. TỔNG KẾT CHIẾN LƯỢC & KHUYẾN NGHỊ TĂNG TRƯỞNG 2026
# ==============================================================================
add_md("""---
## 🎯 Tổng Kết Chiến Lược & Khuyến Nghị Tăng Trưởng Doanh Thu 2026

Từ bức tranh trực quan toàn cảnh năm 2025, chúng tôi khuyến nghị 4 giải pháp kinh doanh chiến lược cho Studio Cưới:

1. **Chiến lược Upsell "Bàn đạp" từ Gói Studio lên Ngoại cảnh:**
   - Gói Studio thu hút hơn 50% lượng khách nhưng chỉ mang lại 26.6% doanh thu. Studio nên tung ra chính sách: *Khách đặt gói Studio được ưu đãi nâng cấp lên Phim trường/Ngoại cảnh với voucher giảm 15%*, giúp tăng giá trị đơn hàng AOV từ 5 triệu lên 10 - 20 triệu.
2. **Tối ưu ngân sách quảng cáo theo tính mùa vụ cưới:**
   - Dồn 70% ngân sách marketing vào 2 mùa vàng: Tháng 10 - 12 (đón cưới Tết) và Tháng 4 - 5 (mùa cưới hè).
   - Riêng **Tháng 8 (Tháng Ngâu)**: Không cắt giảm hoàn toàn quảng cáo mà chuyển sang truyền thông chiến dịch *"Đặt cọc sớm nhận ưu đãi khủng cho tiệc cưới cuối năm"*, giải quyết bài toán dòng tiền thấp điểm.
3. **Đẩy mạnh sáng tạo nội dung Video ngắn trên TikTok:**
   - Tệp khách TikTok có xu hướng chọn gói cao cấp Ngoại cảnh cao nhất (21.8%). Cần đầu tư sản xuất các series hậu trường (behind-the-scenes), chia sẻ khoảnh khắc xúc động để gia tăng tỷ lệ chuyển đổi tự nhiên.
4. **Mở rộng chương trình "Khách cũ giới thiệu khách mới" (Referral Program):**
   - Kênh Người quen mang lại hơn 9.19 tỷ VNĐ doanh thu hoàn toàn miễn phí chi phí quảng cáo. Tặng voucher chụp ảnh gia đình hoặc kỷ niệm ngày cưới cho các cặp đôi giới thiệu bạn bè sẽ giúp nhân rộng kênh tiếp thị hiệu quả này.
""")

print(f"Tổng số cell đã định nghĩa: {len(cells)}")

# ==============================================================================
# THỰC THI CODE & TẠO OUTPUT CHO NOTEBOOK
# ==============================================================================
print("Bắt đầu thực thi các code cell để tạo outputs tương tác...")

cur_dir = os.getcwd()
os.chdir(BASE_DIR)

exec_globals = {}
exec_globals["__file__"] = NB_PATH

executed_cells = []
cell_code_idx = 0

for idx, cell in enumerate(cells):
    if cell.cell_type == "markdown":
        executed_cells.append(cell)
    elif cell.cell_type == "code":
        cell_code_idx += 1
        code_str = cell.source
        
        stdout_buf = io.StringIO()
        captured_figs = []
        
        def custom_show(self, *args, **kwargs):
            captured_figs.append(self)
        
        old_fig_show = go.Figure.show
        go.Figure.show = custom_show
        
        try:
            with contextlib.redirect_stdout(stdout_buf):
                exec(code_str, exec_globals)
        except Exception as e:
            print(f"❌ Lỗi tại Code Cell {cell_code_idx}: {e}")
            raise e
        finally:
            go.Figure.show = old_fig_show
            
        stdout_text = stdout_buf.getvalue()
        outputs = []
        
        if stdout_text.strip():
            outputs.append(nbf.v4.new_output(
                output_type="stream",
                name="stdout",
                text=stdout_text
            ))
            
        for fig in captured_figs:
            html_str = pio.to_html(fig, include_plotlyjs="cdn", full_html=False)
            fig_dict = json.loads(fig.to_json())
            outputs.append(nbf.v4.new_output(
                output_type="display_data",
                data={
                    "text/html": html_str,
                    "application/vnd.plotly.v1+json": fig_dict,
                    "text/plain": [f"Figure({fig.__class__.__name__})"]
                }
            ))
            
        cell.outputs = outputs
        cell.execution_count = cell_code_idx
        executed_cells.append(cell)
        print(f"  ✓ Đã chạy xong Code Cell {cell_code_idx} (Bắt được {len(captured_figs)} biểu đồ Plotly)")

nb = nbf.v4.new_notebook()
nb.cells = executed_cells
nb.metadata = {
    "kernelspec": {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3"
    },
    "language_info": {
        "codemirror_mode": {"name": "ipython", "version": 3},
        "file_extension": ".py",
        "mimetype": "text/x-python",
        "name": "python",
        "nbconvert_exporter": "python",
        "pygments_lexer": "ipython3",
        "version": "3.14.0"
    }
}

with open(NB_PATH, "w", encoding="utf-8") as f:
    nbf.write(nb, f)

print(f"🎉 ĐÃ TẠO VÀ THỰC THI THÀNH CÔNG: {NB_PATH}")
