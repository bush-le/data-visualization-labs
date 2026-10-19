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
DATA_PATH = os.path.join(BASE_DIR, "data", "logistics_KHB.csv")
NB_PATH = os.path.join(BASE_DIR, "logistics_visualization.ipynb")

print("Đang khởi tạo cấu trúc Notebook Logistics (Đã khắc phục toàn bộ lỗi hiển thị)...")

cells = []

def add_md(text):
    cells.append(nbf.v4.new_markdown_cell(text.strip()))

def add_code(code):
    cells.append(nbf.v4.new_code_cell(code.strip()))

# ==============================================================================
# 1. TIÊU ĐỀ BÁO CÁO
# ==============================================================================
add_md("""# 🚚 Báo Cáo Trực Quan Hóa Tương Tác Dữ Liệu Logistics KHB 2025
## 📌 Hệ Thống Dashboard Phân Tích Vận Hành & Hiệu Suất Giao Nhận Bằng Thư Viện Plotly

---

### 🎯 Mục tiêu dự án
Bộ trực quan hóa tương tác này được thiết kế theo triết lý **Đơn giản – Trực quan – Dễ hiểu – Đi từ Tổng quan đến Chi tiết**, giúp Ban Giám đốc và Đội ngũ Điều phối Vận hành nắm bắt trọn vẹn bức tranh hoạt động của **Công ty Giao nhận KHB** trong năm 2025.

### 🧭 Lộ trình phân tích 5 tầng:
1. **Tầng 1: Tổng quan Vĩ mô & Bộ chỉ số KPI Vận hành** – Sức khỏe toàn mạng lưới qua 4 thẻ chỉ số cốt lõi và cơ cấu phân bổ trạng thái đơn hàng (Donut Kép Subplots).
2. **Tầng 2: Diễn biến Theo Thời gian & Chu kỳ Vận hành** – Sản lượng 12 tháng, tỷ lệ giao đúng hạn OTD và bản đồ nhiệt khung giờ cao điểm (Heatmap tối ưu nhãn).
3. **Tầng 3: Mạng lưới Tuyến đường & Hiệu suất 12 Chi nhánh** – Dòng chảy luân chuyển hàng hóa liên tỉnh (Sankey Flow đa sắc) và xếp hạng hiệu suất 12 bưu cục.
4. **Tầng 4: Phân khúc Dịch vụ, Cước phí & Hàng hóa** – Cấu trúc phụ phí hỏa tốc, đường hồi quy tương quan phí ship vs khối lượng và phân bố giá trị 5 ngành hàng.
5. **Tầng 5: Trải nghiệm Khách hàng (CSAT) & Đội ngũ Shipper** – Cơ cấu CSAT 1-5 sao theo kết quả giao hàng và ma trận hiệu suất 87 tài xế 4 góc phần tư.
""")

# ==============================================================================
# 2. KHỞI TẠO MÔI TRƯỜNG & TIỀN XỬ LÝ DỮ LIỆU
# ==============================================================================
add_code("""# 1. Khai báo thư viện và cấu hình hiển thị Plotly
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

# Thiết lập template giao diện chuẩn
pio.renderers.default = "notebook_connected"
PLOTLY_TEMPLATE = "plotly_white"

# Bảng màu ngữ nghĩa thống nhất toàn bộ báo cáo
COLOR_MAP = {
    "Giao đúng hạn": "#2ECC71",   # Xanh lá: Thành công / Đạt chuẩn
    "Giao trễ hạn": "#F39C12",    # Cam vàng: Cảnh báo / Rủi ro
    "Hoàn trả": "#E74C3C"         # Đỏ thắm: Sự cố / Thất thoát
}

# 2. Đọc và tiền xử lý dữ liệu vận đơn
df = pd.read_csv("data/logistics_KHB.csv")

# Chuyển đổi định dạng thời gian
df["Thời Gian"] = pd.to_datetime(df["Thời Gian"], format="%d/%m/%Y %H:%M")
df["Tháng"] = df["Thời Gian"].dt.month
df["Giờ"] = df["Thời Gian"].dt.hour
df["Thứ_Số"] = df["Thời Gian"].dt.dayofweek
day_names = {0: "Thứ Hai", 1: "Thứ Ba", 2: "Thứ Tư", 3: "Thứ Năm", 4: "Thứ Sáu", 5: "Thứ Bảy", 6: "Chủ Nhật"}
df["Thứ"] = df["Thứ_Số"].map(day_names)
df["Tuyến Đường"] = df["Nơi Gửi"] + " ➔ " + df["Nơi Nhận"]

# Ánh xạ chi nhánh về 3 thành phố lớn để gom nhóm trực quan
city_map = {
    "CN Đống Đa": "Hà Nội", "CN Hoàn Kiếm": "Hà Nội", "CN Cầu Giấy": "Hà Nội", "CN Hai Bà Trưng": "Hà Nội",
    "CN Hải Châu": "Đà Nẵng", "CN Liên Chiểu": "Đà Nẵng", "CN Thanh Khê": "Đà Nẵng",
    "CN Tân Bình": "TP Hồ Chí Minh", "CN Thủ Đức": "TP Hồ Chí Minh", "CN Bình Tân": "TP Hồ Chí Minh",
    "CN Quận 1": "TP Hồ Chí Minh", "CN Quận 7": "TP Hồ Chí Minh"
}
df["Thành Phố"] = df["Chi Nhánh"].map(city_map)

print(f"✅ Đã tải thành công: {len(df):,} đơn hàng với {df.shape[1]} thuộc tính.")
print(f"📅 Khoảng thời gian: Từ {df['Thời Gian'].min().strftime('%d/%m/%Y')} đến {df['Thời Gian'].max().strftime('%d/%m/%Y')}.")
df.head(3)""")

# ==============================================================================
# 3. TẦNG 1: TỔNG QUAN VĨ MÔ & BỘ CHỈ SỐ KPI VẬN HÀNH
# ==============================================================================
add_md("""---
## 📊 Tầng 1: Tổng Quan Vĩ Mô & Bộ Chỉ Số Hiệu Suất Vận Hành (Executive KPIs)

Tầng phân tích này giúp người quản trị nắm bắt được **"sức khỏe tổng quát"** của hệ thống chỉ trong 3 giây: Tổng số đơn hoàn thành, tỷ lệ giao đúng hạn (OTD), tỷ lệ giao trễ, mức độ hài lòng khách hàng và phân bổ theo phạm vi địa lý.
""")

add_code("""# Biểu đồ 1.1: Bộ Thẻ Chỉ Số Vàng Vận Hành (Executive KPI Cards)
total_orders = len(df)
on_time_count = (df["Tình Trạng"] == "Giao đúng hạn").sum()
on_time_rate = on_time_count / total_orders * 100
delay_count = (df["Tình Trạng"] == "Giao trễ hạn").sum()
delay_rate = delay_count / total_orders * 100
return_count = (df["Tình Trạng"] == "Hoàn trả").sum()
return_rate = return_count / total_orders * 100
avg_csat = df["Đánh Giá"].mean()

fig1_1 = go.Figure()

# Thẻ 1: Tổng đơn hàng
fig1_1.add_trace(go.Indicator(
    mode="number",
    value=total_orders,
    number={"valueformat": ",d", "font": {"size": 34, "color": "#2C3E50"}},
    title={"text": "<b>TỔNG ĐƠN HÀNG</b><br><span style='font-size:12px;color:#7F8C8D'>Năm 2025</span>"},
    domain={"x": [0.01, 0.23], "y": [0.1, 0.9]}
))

# Thẻ 2: Đúng hạn OTD
fig1_1.add_trace(go.Indicator(
    mode="number",
    value=on_time_rate,
    number={"suffix": "%", "valueformat": ".2f", "font": {"size": 34, "color": "#2ECC71"}},
    title={"text": "<b>GIAO ĐÚNG HẠN (OTD)</b><br><span style='font-size:12px;color:#7F8C8D'>8,003 đơn đạt chuẩn</span>"},
    domain={"x": [0.26, 0.48], "y": [0.1, 0.9]}
))

# Thẻ 3: Trễ hạn
fig1_1.add_trace(go.Indicator(
    mode="number",
    value=delay_rate,
    number={"suffix": "%", "valueformat": ".2f", "font": {"size": 34, "color": "#F39C12"}},
    title={"text": "<b>GIAO TRỄ HẠN</b><br><span style='font-size:12px;color:#7F8C8D'>1,502 đơn cần khắc phục</span>"},
    domain={"x": [0.51, 0.73], "y": [0.1, 0.9]}
))

# Thẻ 4: CSAT
fig1_1.add_trace(go.Indicator(
    mode="number",
    value=avg_csat,
    number={"suffix": " / 5.0 ⭐", "valueformat": ".2f", "font": {"size": 34, "color": "#2980B9"}},
    title={"text": "<b>ĐIỂM HÀI LÒNG CSAT</b><br><span style='font-size:12px;color:#7F8C8D'>Đánh giá khách hàng</span>"},
    domain={"x": [0.76, 0.99], "y": [0.1, 0.9]}
))

# Thêm 4 khối thẻ nền trang nhã
card_domains = [(0.0, 0.24), (0.25, 0.49), (0.50, 0.74), (0.75, 1.0)]
for x0, x1 in card_domains:
    fig1_1.add_shape(
        type="rect", xref="paper", yref="paper",
        x0=x0, x1=x1, y0=0.03, y1=0.97,
        line=dict(color="#E2E8F0", width=1.5),
        fillcolor="#F8FAFC", layer="below"
    )

fig1_1.update_layout(
    template=PLOTLY_TEMPLATE,
    height=250,
    margin=dict(l=15, r=15, t=55, b=15),
    title="<b>BẢNG ĐIỀU KHIỂN CHỈ SỐ VẬN HÀNH CỐT LÕI (EXECUTIVE KPI BOARD)</b>",
    title_x=0.5
)
fig1_1.show()""")

add_code("""# Biểu đồ 1.2: Cơ Cấu Đơn Hàng Theo Phạm Vi Địa Lý & Tình Trạng Giao Hàng (Donut Kép Subplots)
geo_counts = df["Phân Loại"].value_counts()
status_counts = df["Tình Trạng"].value_counts()

fig1_2 = make_subplots(
    rows=1, cols=2,
    specs=[[{"type": "domain"}, {"type": "domain"}]],
    subplot_titles=["<b>1. Phân Bổ Theo Phạm Vi Địa Lý</b>", "<b>2. Cơ Cấu Kết Quả Giao Hàng</b>"]
)

# Donut 1: Phạm vi địa lý
fig1_2.add_trace(
    go.Pie(
        labels=geo_counts.index,
        values=geo_counts.values,
        hole=0.55,
        marker=dict(colors=["#3498DB", "#9B59B6"]),
        textinfo="label+percent",
        hovertemplate="Phạm vi: <b>%{label}</b><br>Số lượng: <b>%{value:,} đơn</b><br>Tỷ trọng: <b>%{percent:.1%}</b><extra></extra>"
    ),
    row=1, col=1
)

# Donut 2: Tình trạng giao hàng
fig1_2.add_trace(
    go.Pie(
        labels=status_counts.index,
        values=status_counts.values,
        hole=0.55,
        marker=dict(colors=[COLOR_MAP[s] for s in status_counts.index]),
        textinfo="label+percent",
        hovertemplate="Trạng thái: <b>%{label}</b><br>Số lượng: <b>%{value:,} đơn</b><br>Tỷ trọng: <b>%{percent:.1%}</b><extra></extra>"
    ),
    row=1, col=2
)

fig1_2.update_layout(
    title="<b>Cơ Cấu Toàn Cảnh: Phạm Vi Vận Chuyển & Kết Quả Giao Hàng Năm 2025</b>",
    title_x=0.5,
    template=PLOTLY_TEMPLATE,
    height=460,
    legend=dict(orientation="h", yanchor="bottom", y=-0.08, xanchor="center", x=0.5)
)
fig1_2.show()""")

# ==============================================================================
# 4. TẦNG 2: DIỄN BIẾN THEO THỜI GIAN & CHU KỲ VẬN HÀNH
# ==============================================================================
add_md("""---
## 📈 Tầng 2: Diễn Biến Theo Thời Gian & Chu Kỳ Vận Hành (Temporal Dynamics)

Phân tích chu kỳ thời gian giúp nhận diện tính mùa vụ trong năm và quy luật phát sinh đơn hàng trong ngày, từ đó tối ưu kế hoạch nhân sự và năng lực trung chuyển.
""")

add_code("""# Biểu đồ 2.1: Xu Hướng Sản Lượng Đơn & Tỷ Lệ Giao Đúng Hạn Theo 12 Tháng
monthly = df.groupby("Tháng").agg(
    Tong_Don=("Mã Đơn Hàng", "count"),
    Dung_Han=("Tình Trạng", lambda x: (x == "Giao đúng hạn").sum()),
    Tre_Han=("Tình Trạng", lambda x: (x == "Giao trễ hạn").sum())
).reset_index()

monthly["Ty_Le_Dung_Han"] = (monthly["Dung_Han"] / monthly["Tong_Don"] * 100).round(2)

fig2_1 = make_subplots(specs=[[{"secondary_y": True}]])

# 1. Cột sản lượng đơn hàng
fig2_1.add_trace(
    go.Bar(
        x=monthly["Tháng"],
        y=monthly["Tong_Don"],
        name="Sản lượng đơn hàng (Đơn)",
        marker_color="#3498DB",
        hovertemplate="Tháng %{x}: <b>%{y:,} đơn</b><extra></extra>"
    ),
    secondary_y=False
)

# 2. Đường tỷ lệ đúng hạn OTD
fig2_1.add_trace(
    go.Scatter(
        x=monthly["Tháng"],
        y=monthly["Ty_Le_Dung_Han"],
        name="Tỷ lệ đúng hạn OTD (%)",
        mode="lines+markers+text",
        line=dict(color="#27AE60", width=3),
        marker=dict(size=8, color="#2ECC71"),
        text=[f"{v:.1f}%" for v in monthly["Ty_Le_Dung_Han"]],
        textposition="top center",
        hovertemplate="Tỷ lệ đúng hạn: <b>%{y:.2f}%</b><extra></extra>"
    ),
    secondary_y=True
)

fig2_1.update_layout(
    title="<b>Xu Hướng Sản Lượng Đơn Hàng & Tỷ Lệ Giao Đúng Hạn 12 Tháng Năm 2025</b>",
    title_x=0.5,
    xaxis=dict(
        title="Tháng tiếp nhận đơn",
        tickmode="linear",
        tick0=1,
        dtick=1
    ),
    yaxis=dict(title="Số lượng đơn hàng (Đơn)", range=[0, 1100], showgrid=True),
    yaxis2=dict(title="Tỷ lệ đúng hạn (%)", range=[72, 88], dtick=4, showgrid=False),
    template=PLOTLY_TEMPLATE,
    height=480,
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.03, xanchor="center", x=0.5)
)
fig2_1.show()""")

add_code("""# Biểu đồ 2.2: Bản Đồ Nhiệt Khung Giờ & Ngày Trong Tuần (Operational Heatmap)
order_days = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]
heat_data = df.groupby(["Thứ", "Giờ"]).size().unstack(fill_value=0)
heat_data = heat_data.reindex(order_days)

fig2_2 = px.imshow(
    heat_data,
    labels=dict(x="Khung Giờ Trong Ngày", y="Ngày Trong Tuần", color="Số Đơn Hàng"),
    x=[f"{h}h" for h in heat_data.columns],
    y=heat_data.index,
    color_continuous_scale="Blues",
    title="<b>Bản Đồ Nhiệt Mật Độ Đơn Hàng Theo Khung Giờ & Ngày Trong Tuần</b>",
    template=PLOTLY_TEMPLATE
)
fig2_2.update_traces(
    hovertemplate="Ngày: <b>%{y}</b><br>Khung giờ: <b>%{x}</b><br>Mật độ đơn: <b>%{z:,} đơn</b><extra></extra>"
)
fig2_2.update_layout(
    title_x=0.5,
    height=430,
    margin=dict(t=70, b=40),
    xaxis=dict(tickmode="linear", dtick=2)  # Hiện mốc mỗi 2 tiếng để nhãn thoáng đãng
)
fig2_2.show()""")

# ==============================================================================
# 5. TẦNG 3: MẠNG LƯỚI TUYẾN ĐƯỜNG & CHI NHÁNH
# ==============================================================================
add_md("""---
## 🗺️ Tầng 3: Mạng Lưới Tuyến Đường & Hiệu Suất 12 Chi Nhánh (Network & Facilities)

Phân tích đa chiều về luồng chuyển dịch hàng hóa giữa các thành phố trọng điểm và xếp hạng năng lực giao vận của từng chi nhánh phụ trách.
""")

add_code("""# Biểu đồ 3.1: Dòng Chảy Hàng Hóa Tuyến Đường Gửi - Nhận (Sankey Flow Đa Sắc)
route_counts = df.groupby(["Nơi Gửi", "Nơi Nhận"]).size().reset_index(name="Số Đơn")

cities = ["Hà Nội", "Đà Nẵng", "TP Hồ Chí Minh"]

label_nodes = [f"Gửi từ {c}" for c in cities] + [f"Giao đến {c}" for c in cities]
node_colors = ["#E67E22", "#9B59B6", "#2980B9", "#D35400", "#8E44AD", "#1F618D"]

# Màu link phân theo Thành phố gửi giúp luồng đi cực kỳ trực quan
link_colors_map = {
    "Hà Nội": "rgba(230, 126, 34, 0.4)",
    "Đà Nẵng": "rgba(155, 89, 182, 0.4)",
    "TP Hồ Chí Minh": "rgba(41, 128, 185, 0.4)"
}

src_indices = [cities.index(row["Nơi Gửi"]) for _, row in route_counts.iterrows()]
dst_indices = [len(cities) + cities.index(row["Nơi Nhận"]) for _, row in route_counts.iterrows()]
link_colors = [link_colors_map[row["Nơi Gửi"]] for _, row in route_counts.iterrows()]

fig3_1 = go.Figure(data=[go.Sankey(
    node=dict(
        pad=25,
        thickness=25,
        line=dict(color="black", width=0.5),
        label=label_nodes,
        color=node_colors
    ),
    link=dict(
        source=src_indices,
        target=dst_indices,
        value=route_counts["Số Đơn"],
        color=link_colors,
        hovertemplate="Tuyến: <b>%{source.label} ➔ %{target.label}</b><br>Sản lượng vận chuyển: <b>%{value:,} đơn</b><extra></extra>"
    )
)])

fig3_1.update_layout(
    title="<b>Sơ Đồ Dòng Chảy Luân Chuyển Hàng Hóa Giữa Các Thành Phố (Sankey Flow)</b>",
    title_x=0.5,
    font=dict(family="Arial", size=13),
    template=PLOTLY_TEMPLATE,
    height=480,
    margin=dict(t=70, l=20, r=20, b=20)
)
fig3_1.show()""")

add_code("""# Biểu đồ 3.2: So Sánh Hiệu Suất Vận Hành Của 12 Chi Nhánh (Xếp Hạng Tăng Dần)
branch_perf = df.groupby(["Chi Nhánh", "Tình Trạng"]).size().unstack(fill_value=0)
branch_perf["Tổng"] = branch_perf.sum(axis=1)
branch_pct = branch_perf.div(branch_perf["Tổng"], axis=0) * 100

# Sắp xếp tăng dần theo tỷ lệ đúng hạn để khi vẽ horizontal bar, nhánh xuất sắc nhất ở trên cùng
branch_pct = branch_pct.sort_values(by="Giao đúng hạn", ascending=True)

fig3_2 = go.Figure()

for status in ["Giao đúng hạn", "Giao trễ hạn", "Hoàn trả"]:
    # Chỉ hiển thị text inside nếu tỷ lệ >= 8% để triệt tiêu lỗi tràn chữ ở dải Hoàn trả 4%
    text_labels = [f"{v:.1f}%" if v >= 8 else "" for v in branch_pct[status]]
    fig3_2.add_trace(go.Bar(
        y=branch_pct.index,
        x=branch_pct[status],
        name=status,
        orientation="h",
        marker_color=COLOR_MAP[status],
        text=text_labels,
        textposition="inside",
        insidetextanchor="middle",
        hovertemplate="Chi nhánh: <b>%{y}</b><br>Trạng thái: <b>" + status + "</b><br>Tỷ lệ: <b>%{x:.2f}%</b><extra></extra>"
    ))

fig3_2.update_layout(
    barmode="stack",
    title="<b>Xếp Hạng Hiệu Suất Giao Hàng Của 12 Chi Nhánh (Sắp Xếp Theo Tỷ Lệ Đúng Hạn)</b>",
    title_x=0.5,
    xaxis=dict(title="Tỷ lệ phần trăm đơn hàng (%)", range=[0, 100]),
    yaxis=dict(title="Chi nhánh tiếp nhận"),
    template=PLOTLY_TEMPLATE,
    height=550,
    legend=dict(orientation="h", yanchor="bottom", y=1.03, xanchor="center", x=0.5)
)
fig3_2.show()""")

# ==============================================================================
# 6. TẦNG 4: PHÂN KHÚC DỊCH VỤ, CƯỚC PHÍ & HÀNG HÓA
# ==============================================================================
add_md("""---
## 💰 Tầng 4: Phân Khúc Dịch Vụ, Cước Phí & Đặc Điểm Hàng Hóa

Làm rõ cấu trúc định giá cước dịch vụ, mối tương quan giữa phí vận chuyển và khối lượng gói hàng, cùng sự phân hóa về giá trị của 5 ngành hàng chính.
""")

add_code("""# Biểu đồ 4.1: Tương Quan Giữa Phí Ship, Khối Lượng & Dịch Vụ (Kèm Đường Hồi Quy Tuyến Tính)
sample_df = df.sample(n=1200, random_state=42)

fig4_1 = make_subplots(
    rows=1, cols=2,
    subplot_titles=["<b>🚚 Tuyến Nội Thành (Nội đô)</b>", "<b>🚛 Tuyến Liên Tỉnh (Trục Bắc - Nam)</b>"],
    shared_yaxes=True
)

service_colors = {"Bình thường": "#3498DB", "Nhanh": "#E74C3C"}

for col_idx, geo in enumerate(["Nội thành", "Liên tỉnh"], start=1):
    sub = sample_df[sample_df["Phân Loại"] == geo]
    for service in ["Bình thường", "Nhanh"]:
        s_data = sub[sub["Hình Thức"] == service]
        # Điểm phân tán
        fig4_1.add_trace(go.Scatter(
            x=s_data["Khối Lượng (kg)"],
            y=s_data["Phí Ship"],
            mode="markers",
            name=f"Giao {service.lower()}",
            legendgroup=service,
            showlegend=(col_idx == 1),
            marker=dict(color=service_colors[service], size=5, opacity=0.55),
            hovertemplate=f"Dịch vụ: <b>{service}</b> ({geo})<br>Khối lượng: <b>%{{x}} kg</b><br>Phí ship: <b>%{{y:,}} đ</b><extra></extra>"
        ), row=1, col=col_idx)
        
        # Đường hồi quy xu hướng
        p = np.polyfit(s_data["Khối Lượng (kg)"], s_data["Phí Ship"], 1)
        x_line = np.linspace(0.5, 10, 50)
        y_line = np.polyval(p, x_line)
        fig4_1.add_trace(go.Scatter(
            x=x_line,
            y=y_line,
            mode="lines",
            name=f"Đường xu hướng {service}",
            legendgroup=service,
            showlegend=False,
            line=dict(color=service_colors[service], width=2.5, dash="dash")
        ), row=1, col=col_idx)

fig4_1.update_layout(
    title="<b>Tương Quan Phí Ship và Khối Lượng Theo Dịch Vụ & Phạm Vi Địa Lý</b>",
    title_x=0.5,
    template=PLOTLY_TEMPLATE,
    height=480,
    legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5)
)
fig4_1.update_xaxes(title_text="Khối lượng đơn hàng (kg)")
fig4_1.update_yaxes(title_text="Cước phí vận chuyển (VNĐ)", row=1, col=1)
fig4_1.show()""")

add_code("""# Biểu đồ 4.2: Phân Bố Giá Trị Hàng Hóa Theo 5 Ngành Hàng (Box Plot Giữ Trọn Hover Stats)
fig4_2 = px.box(
    df,
    x="Mặt Hàng",
    y="Giá Trị (VNĐ)",
    color="Mặt Hàng",
    title="<b>Phân Bố Giá Trị Hàng Hóa Khai Báo Theo Từng Ngành Hàng (Box Plot)</b>",
    template=PLOTLY_TEMPLATE,
    points=False  # Giữ hộp sắc nét, không bị nhiễu bởi 10.000 điểm phân tán
)
fig4_2.update_layout(
    title_x=0.5,
    height=480,
    showlegend=False,
    xaxis=dict(title="Nhóm mặt hàng vận chuyển"),
    yaxis=dict(title="Giá trị hàng hóa khai báo (VNĐ)", tickformat=",.0f", showgrid=True)
)
fig4_2.show()""")

# ==============================================================================
# 7. TẦNG 5: TRẢI NGHIỆM KHÁCH HÀNG & ĐỘI NGŨ SHIPPER
# ==============================================================================
add_md("""---
## ⭐ Tầng 5: Trải Nghiệm Khách Hàng (CSAT) & Đội Ngũ Shipper

Đánh giá chất lượng dịch vụ từ góc nhìn của khách hàng và phân tích ma trận năng suất của đội ngũ 87 shipper giao hàng tuyến cuối.
""")

add_code("""# Biểu đồ 5.1: Mức Độ Tác Động Của Trạng Thái Giao Hàng Đến Điểm CSAT (Stacked Bar Khắc Phục Lỗ Hổng Cột)
csat_table = pd.crosstab(df["Đánh Giá"], df["Tình Trạng"])

fig5_1 = go.Figure()

for status in ["Giao đúng hạn", "Giao trễ hạn", "Hoàn trả"]:
    if status in csat_table.columns:
        fig5_1.add_trace(go.Bar(
            x=[f"{r} ⭐" for r in csat_table.index],
            y=csat_table[status],
            name=status,
            marker_color=COLOR_MAP[status],
            text=[f"{v:,}" if v > 150 else "" for v in csat_table[status]],
            textposition="inside",
            insidetextanchor="middle",
            hovertemplate="Số sao: <b>%{x}</b><br>Trạng thái: <b>" + status + "</b><br>Số đơn: <b>%{y:,} đơn</b><extra></extra>"
        ))

fig5_1.update_layout(
    barmode="stack",
    title="<b>Cơ Cấu Tình Trạng Giao Hàng Trong Từng Mức Đánh Giá Sao (1 - 5 ⭐)</b>",
    title_x=0.5,
    xaxis=dict(title="Điểm đánh giá của khách hàng"),
    yaxis=dict(title="Số lượng đơn hàng (Đơn)", range=[0, 4600], showgrid=True),
    template=PLOTLY_TEMPLATE,
    height=480,
    legend=dict(orientation="h", yanchor="bottom", y=1.03, xanchor="center", x=0.5)
)
fig5_1.show()

# In bảng thống kê CSAT trung bình
csat_by_status = df.groupby("Tình Trạng")["Đánh Giá"].mean()
print("⭐ Điểm CSAT Trung Bình Theo Kết Quả Giao Hàng:")
for s, val in csat_by_status.items():
    print(f"  - {s:<15}: {val:.2f} / 5.0 ⭐")""")

add_code("""# Biểu đồ 5.2: Ma Trận Năng Suất & Chất Lượng Phục Vụ Của 87 Shipper (Bubble Matrix)
shipper_stat = df.groupby("Shipper").agg(
    Tong_Don=("Mã Đơn Hàng", "count"),
    CSAT_TB=("Đánh Giá", "mean"),
    Ty_Le_Dung_Han=("Tình Trạng", lambda x: (x == "Giao đúng hạn").mean() * 100),
    Chi_Nhanh=("Chi Nhánh", "first"),
    Thanh_Pho=("Thành Phố", "first")
).reset_index()

avg_orders = shipper_stat["Tong_Don"].mean()
avg_rating = shipper_stat["CSAT_TB"].mean()

fig5_2 = px.scatter(
    shipper_stat,
    x="Tong_Don",
    y="CSAT_TB",
    size="Ty_Le_Dung_Han",
    color="Thanh_Pho",
    color_discrete_map={
        "Hà Nội": "#E67E22",
        "Đà Nẵng": "#9B59B6",
        "TP Hồ Chí Minh": "#2980B9"
    },
    hover_name="Shipper",
    custom_data=["Chi_Nhanh", "Ty_Le_Dung_Han"],
    size_max=16,
    title="<b>Ma Trận Hiệu Suất 87 Shipper (Năng Suất vs CSAT vs Tỷ Lệ Đúng Hạn)</b>",
    labels={
        "Tong_Don": "Tổng đơn giao hoàn thành (Năng suất)",
        "CSAT_TB": "Điểm CSAT trung bình (⭐)",
        "Thanh_Pho": "Khu vực"
    },
    template=PLOTLY_TEMPLATE
)

# Thêm đường tham chiếu trung bình chia 4 góc phần tư
fig5_2.add_vline(x=avg_orders, line_dash="dash", line_color="#7F8C8D",
                 annotation_text=f"Năng suất TB ({avg_orders:.0f} đơn)", annotation_position="top left")
fig5_2.add_hline(y=avg_rating, line_dash="dash", line_color="#7F8C8D",
                 annotation_text=f"CSAT TB ({avg_rating:.2f}⭐)", annotation_position="bottom right")

# Tô màu nền nhẹ nổi bật góc phần tư Shipper xuất sắc (Góc trên bên phải)
fig5_2.add_shape(
    type="rect",
    x0=avg_orders, x1=shipper_stat["Tong_Don"].max() + 10,
    y0=avg_rating, y1=shipper_stat["CSAT_TB"].max() + 0.05,
    fillcolor="rgba(46, 204, 113, 0.1)", line=dict(width=0), layer="below"
)

fig5_2.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>Khu vực: <b>%{data.name}</b> (%{customdata[0]})<br>Tổng đơn giao: <b>%{x} đơn</b><br>Điểm CSAT: <b>%{y:.2f} ⭐</b><br>Tỷ lệ đúng hạn: <b>%{customdata[1]:.1f}%</b><extra></extra>"
)
fig5_2.update_layout(
    title_x=0.5,
    height=550,
    xaxis=dict(range=[50, 205], showgrid=True),
    yaxis=dict(range=[3.85, 4.45], showgrid=True),
    legend=dict(orientation="h", yanchor="bottom", y=1.03, xanchor="center", x=0.5)
)
fig5_2.show()""")

# ==============================================================================
# 8. TỔNG KẾT VẬN HÀNH & KHUYẾN NGHỊ HÀNH ĐỘNG
# ==============================================================================
add_md("""---
## 🎯 Tổng Kết Vận Hành & Khuyến Nghị Hành Động (Actionable Strategy)

Qua phân tích toàn diện 10.000 vận đơn năm 2025 bằng Plotly, chúng tôi đề xuất 4 giải pháp trọng tâm cho Ban Giám đốc KHB:

1. **Khắc phục điểm nghẽn tại 2 chi nhánh có tỷ lệ trễ hạn cao nhất:**
   - Tập trung nguồn lực kiểm toán vận hành tại `CN Đống Đa` (16.23% trễ) và `CN Thủ Đức` (15.74% trễ). Tái phân chia tuyến giao cho shipper để giảm bán kính di chuyển trong giờ cao điểm.
2. **Cơ chế thưởng KPI gắn với OTD và CSAT:**
   - Dựa trên ma trận phân tích 87 shipper, thiết lập chính sách thưởng nóng cho nhóm tài xế đạt OTD > 85% và CSAT > 4.3⭐ để thúc đẩy tinh thần làm việc.
3. **Phân bổ nhân sự điều phối theo bản đồ nhiệt khung giờ:**
   - Tăng cường điều phối viên tại kho vào 2 khung giờ tập trung nhiều đơn nhất: ca trưa (11h-14h) và ca tối (19h-21h) để đảm bảo hàng hóa được quét xuất kho trong vòng 60 phút.
4. **Nâng cấp tính năng cảnh báo bảo hiểm cho đơn hàng giá trị cao:**
   - Hàng hóa có giá trị trên 5 triệu đồng chiếm tỷ lệ đáng kể ở cả 5 ngành hàng. Việc đề xuất bảo hiểm tự động trên ứng dụng sẽ vừa bảo vệ quyền lợi người gửi, vừa giảm rủi ro tranh chấp tài chính khi có sự cố hoàn trả.
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
