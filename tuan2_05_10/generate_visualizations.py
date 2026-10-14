import os
import shutil
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Thiết lập font và style hiển thị
plt.rcParams['font.sans-serif'] = ['Liberation Sans', 'DejaVu Sans', 'Arial']
plt.rcParams['axes.unicode_minus'] = False
plt.style.use('seaborn-v0_8-whitegrid')

colors = {
    'Gold': '#F59E0B',       # Vàng ánh kim
    'Silver': '#94A3B8',     # Bạc sáng
    'Bronze': '#D97706',     # Đồng đậm
    'Honourable': '#CBD5E1'  # Bằng khen
}

color_rank = '#DC2626'  # Đỏ đậm cho Thứ hạng
color_score = '#2563EB' # Xanh dương cho Điểm số

def render_charts_for_dataset(csv_path, output_dir, period_label):
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(csv_path)

    # ---------------------------------------------------------
    # 1. CHART 1: STACKED BAR CHART (Clean Design)
    # ---------------------------------------------------------
    fig, ax = plt.subplots(figsize=(11, 5.8), dpi=300)
    p1 = ax.bar(df['Year'], df['Gold'], label='Huy chương Vàng (Gold)', color=colors['Gold'], width=0.55, edgecolor='white', linewidth=1)
    p2 = ax.bar(df['Year'], df['Silver'], bottom=df['Gold'], label='Huy chương Bạc (Silver)', color=colors['Silver'], width=0.55, edgecolor='white', linewidth=1)
    p3 = ax.bar(df['Year'], df['Bronze'], bottom=df['Gold'] + df['Silver'], label='Huy chương Đồng (Bronze)', color=colors['Bronze'], width=0.55, edgecolor='white', linewidth=1)
    p4 = ax.bar(df['Year'], df['Honourable'], bottom=df['Gold'] + df['Silver'] + df['Bronze'], label='Bằng khen (Honourable Mention)', color=colors['Honourable'], width=0.55, edgecolor='white', linewidth=1)

    for i, row in df.iterrows():
        y_accum = 0
        for col, c in [('Gold', 'black'), ('Silver', 'black'), ('Bronze', 'white'), ('Honourable', 'black')]:
            val = row[col]
            if val > 0:
                ax.text(row['Year'], y_accum + val / 2, f"{val}", ha='center', va='center', color=c, fontweight='bold', fontsize=10.5)
                y_accum += val

    ax.set_title(f"Cơ Cấu Huy Chương Đội Tuyển IMO Việt Nam ({period_label})", fontsize=15, fontweight='bold', pad=20, color='#0F172A')
    ax.set_xlabel("Năm", fontsize=11, fontweight='bold', labelpad=10, color='#334155')
    ax.set_ylabel("Số lượng thí sinh / Giải thưởng (Quy mô 6 thí sinh/năm)", fontsize=11, fontweight='bold', labelpad=10, color='#334155')
    ax.set_xticks(df['Year'])
    ax.set_ylim(0, 6.6)
    ax.legend(frameon=True, facecolor='#F8FAFC', edgecolor='none', loc='upper right', fontsize=10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    plt.tight_layout()
    chart1_path = os.path.join(output_dir, "01_co_cau_huy_chuong.png")
    plt.savefig(chart1_path)
    plt.close()
    print("Saved:", chart1_path)

    # ---------------------------------------------------------
    # 2. CHART 2: 2 SUBPLOTS SONG SONG (TRIỆT TIÊU 100% ĐÈ CHỮ)
    # ---------------------------------------------------------
    fig, (ax_r, ax_s) = plt.subplots(2, 1, figsize=(11.5, 7.8), dpi=300, sharex=True)

    # Subplot trên: Thứ hạng toàn đoàn
    ax_r.set_ylim(37, 0) # Đảo trục: Hạng 1 ở trên cùng
    ax_r.plot(df['Year'], df['Rank'], color=color_rank, marker='o', linewidth=2.5, markersize=8, label='Thứ hạng toàn đoàn thế giới')
    ax_r.set_ylabel("Thứ hạng (Càng cao càng tốt)", color=color_rank, fontsize=11, fontweight='bold', labelpad=10)
    ax_r.tick_params(axis='y', labelcolor=color_rank)
    ax_r.grid(True, linestyle=':', alpha=0.6)

    for i, row in df.iterrows():
        # Trục đảo ngược: giá trị âm dịch lên trên, dương dịch xuống dưới
        offset = -14 if row['Rank'] <= 15 else 14
        ax_r.annotate(
            f"Hạng {row['Rank']}",
            xy=(row['Year'], row['Rank']),
            xytext=(0, offset),
            textcoords="offset points",
            ha='center', va='center',
            fontsize=9.5, fontweight='bold', color=color_rank,
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=color_rank, lw=1.2, alpha=0.95),
            zorder=5
        )
    ax_r.set_title(f"1. Biến Động Thứ Hạng Toàn Đoàn IMO ({period_label})", fontsize=13, fontweight='bold', loc='left', color='#0F172A')

    # Subplot dưới: Tổng điểm đội tuyển
    ax_s.set_ylim(100, 215)
    ax_s.plot(df['Year'], df['Total_Score'], color=color_score, marker='s', linewidth=2.5, linestyle='--', markersize=7.5, label='Tổng điểm đội tuyển (Điểm tối đa 252)')
    ax_s.set_xlabel("Năm", fontsize=11, fontweight='bold', labelpad=10, color='#334155')
    ax_s.set_ylabel("Tổng điểm đội tuyển", color=color_score, fontsize=11, fontweight='bold', labelpad=10)
    ax_s.tick_params(axis='y', labelcolor=color_score)
    ax_s.set_xticks(df['Year'])
    ax_s.grid(True, linestyle=':', alpha=0.6)

    for i, row in df.iterrows():
        offset = 14 if row['Total_Score'] <= 160 else -14
        ax_s.annotate(
            f"{row['Total_Score']}đ",
            xy=(row['Year'], row['Total_Score']),
            xytext=(0, offset),
            textcoords="offset points",
            ha='center', va='center',
            fontsize=9.5, fontweight='bold', color=color_score,
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=color_score, lw=1.2, alpha=0.95),
            zorder=5
        )
    ax_s.set_title(f"2. Biến Động Tổng Điểm Đội Tuyển ({period_label})", fontsize=13, fontweight='bold', loc='left', color='#0F172A')

    plt.suptitle(f"SO SÁNH XU HƯỚNG THỨ HẠNG VÀ TỔNG ĐIỂM IMO VIỆT NAM ({period_label})",
                 fontsize=14.5, fontweight='bold', y=0.985, color='#0F172A')
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    chart2_path = os.path.join(output_dir, "02_thu_hang_va_tong_diem.png")
    plt.savefig(chart2_path)
    plt.close()
    print("Saved:", chart2_path)

    # ---------------------------------------------------------
    # 3. CHART 3A: DONUT CHART (TỔNG CƠ CẤU GIẢI THƯỞNG)
    # ---------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8, 6), dpi=300)
    total_gold = df['Gold'].sum()
    total_silver = df['Silver'].sum()
    total_bronze = df['Bronze'].sum()
    total_hon = df['Honourable'].sum()
    sizes = [total_gold, total_silver, total_bronze, total_hon]
    labels_donut = [f'Huy chương Vàng\n({total_gold} giải - {total_gold/sum(sizes)*100:.1f}%)',
                    f'Huy chương Bạc\n({total_silver} giải - {total_silver/sum(sizes)*100:.1f}%)',
                    f'Huy chương Đồng\n({total_bronze} giải - {total_bronze/sum(sizes)*100:.1f}%)',
                    f'Bằng khen\n({total_hon} giải - {total_hon/sum(sizes)*100:.1f}%)']
    colors_donut = [colors['Gold'], colors['Silver'], colors['Bronze'], colors['Honourable']]

    ax.pie(sizes, labels=labels_donut, colors=colors_donut, startangle=140,
           textprops={'fontsize': 10.5, 'fontweight': 'bold', 'color': '#1E293B'},
           wedgeprops=dict(width=0.45, edgecolor='white', linewidth=2.5))
    ax.text(0, 0, f"TỔNG CỘNG\n{sum(sizes)} Lượt\nThí Sinh", ha='center', va='center', fontsize=12, fontweight='bold', color='#334155')
    ax.set_title(f"Tổng Cơ Cấu Giải Thưởng IMO Việt Nam ({period_label})", fontsize=14, fontweight='bold', pad=20, color='#0F172A')
    plt.tight_layout()
    chart3a_path = os.path.join(output_dir, "03_tong_co_cau_giai_thuong.png")
    plt.savefig(chart3a_path)
    plt.close()
    print("Saved:", chart3a_path)

    # ---------------------------------------------------------
    # 4. CHART 3B: BAR CHART (ĐIỂM TRUNG BÌNH MỖI THÍ SINH)
    # ---------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    avg_scores = df['Total_Score'] / 6
    mean_val = avg_scores.mean()

    ax.bar(df['Year'], avg_scores, color='#0284C7', alpha=0.9, width=0.55, edgecolor='white', linewidth=1)
    ax.axhline(mean_val, color='#EF4444', linestyle='--', linewidth=2, label=f"Điểm TB 10 năm: {mean_val:.1f} điểm / học sinh")

    for i, row in df.iterrows():
        s = row['Total_Score'] / 6
        ax.text(row['Year'], s + 0.7, f"{s:.1f}đ", ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#0369A1')

    ax.set_title(f"Điểm Thi Trung Bình Của Mỗi Thí Sinh Việt Nam ({period_label})", fontsize=14, fontweight='bold', pad=20, color='#0F172A')
    ax.set_xlabel("Năm", fontsize=11, fontweight='bold', labelpad=10, color='#334155')
    ax.set_ylabel("Điểm trung bình (Thang điểm tối đa 42)", fontsize=11, fontweight='bold', labelpad=10, color='#334155')
    ax.set_xticks(df['Year'])
    ax.set_ylim(0, 38)
    ax.legend(loc='upper right', frameon=True, facecolor='#F8FAFC', fontsize=10.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    plt.tight_layout()
    chart3b_path = os.path.join(output_dir, "04_diem_trung_binh_thi_sinh.png")
    plt.savefig(chart3b_path)
    plt.close()
    print("Saved:", chart3b_path)

    # ---------------------------------------------------------
    # 5. CHART 3C: HORIZONTAL BAR (TẦN SUẤT THỨ HẠNG)
    # ---------------------------------------------------------
    fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
    bins = [0, 5, 10, 20, 50]
    labels_rank_grp = ['Top 5 Thế Giới', 'Top 6 - 10 Thế Giới', 'Top 11 - 20 Thế Giới', 'Ngoài Top 20']
    df['Rank_Group'] = pd.cut(df['Rank'], bins=bins, labels=labels_rank_grp)
    rank_counts = df['Rank_Group'].value_counts()[labels_rank_grp]

    rank_colors = ['#10B981', '#3B82F6', '#F59E0B', '#EF4444']
    ax.barh(labels_rank_grp[::-1], rank_counts.values[::-1], color=rank_colors[::-1], height=0.52, edgecolor='white')

    for idx, val in enumerate(rank_counts.values[::-1]):
        pct = (val / len(df)) * 100
        ax.text(val + 0.1, idx, f"{val} năm ({pct:.0f}%)", va='center', fontsize=10, fontweight='bold', color='#1E293B')

    ax.set_title(f"Phân Phối Tần Suất Xếp Hạng Toàn Đoàn IMO ({period_label})", fontsize=14, fontweight='bold', pad=20, color='#0F172A')
    ax.set_xlabel("Số năm đạt được", fontsize=11, fontweight='bold', labelpad=10, color='#334155')
    ax.set_xlim(0, 5.2)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='x', linestyle='--', alpha=0.5)

    plt.tight_layout()
    chart3c_path = os.path.join(output_dir, "05_tan_suat_xep_hang_toan_doan.png")
    plt.savefig(chart3c_path)
    plt.close()
    print("Saved:", chart3c_path)

    # ---------------------------------------------------------
    # 6. CHART 3D: SCATTER & REGRESSION (TƯƠNG QUAN ĐIỂM - HẠNG)
    # ---------------------------------------------------------
    fig, ax = plt.subplots(figsize=(9.5, 6), dpi=300)
    sns.regplot(
        data=df, x='Total_Score', y='Rank', ax=ax,
        scatter_kws={'s': 90, 'color': '#7C3AED', 'alpha': 0.85, 'edgecolors': 'white', 'linewidths': 1.5},
        line_kws={'color': '#DC2626', 'linestyle': '--', 'linewidth': 2, 'label': 'Đường xu hướng hồi quy'}
    )

    for i, row in df.iterrows():
        ax.annotate(
            f"Năm {row['Year']}\n(Hạng {row['Rank']})",
            xy=(row['Total_Score'], row['Rank']),
            xytext=(8, -8 if row['Rank'] > 15 else 8),
            textcoords="offset points",
            fontsize=8.5, fontweight='bold', color='#4B5563',
            bbox=dict(boxstyle="round,pad=0.2", fc="#F8FAFC", ec="#E2E8F0", lw=0.8, alpha=0.9)
        )

    ax.set_title(f"Mối Tương Quan: Tổng Điểm vs Thứ Hạng ({period_label})", fontsize=14, fontweight='bold', pad=20, color='#0F172A')
    ax.set_xlabel("Tổng điểm đội tuyển (Tối đa 252)", fontsize=11, fontweight='bold', labelpad=10, color='#334155')
    ax.set_ylabel("Thứ hạng toàn đoàn (Nghịch đảo, Hạng 1 cao nhất)", fontsize=11, fontweight='bold', labelpad=10, color='#334155')
    ax.set_ylim(37, 0)
    ax.legend(loc='lower left', frameon=True, facecolor='#F8FAFC', fontsize=10)
    ax.grid(True, linestyle=':', alpha=0.6)

    plt.tight_layout()
    chart3d_path = os.path.join(output_dir, "06_tuong_quan_diem_va_thu_hang.png")
    plt.savefig(chart3d_path)
    plt.close()
    print("Saved:", chart3d_path)


# Xác định đường dẫn tương đối từ vị trí file script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Render cho cả 2 folder riêng biệt
render_charts_for_dataset(
    os.path.join(BASE_DIR, "data", "vietnam_imo_2017_2026.csv"),
    os.path.join(BASE_DIR, "charts", "period_2017_2026"),
    "2017 - 2026"
)
render_charts_for_dataset(
    os.path.join(BASE_DIR, "data", "vietnam_imo_2015_2024.csv"),
    os.path.join(BASE_DIR, "charts", "period_2015_2024"),
    "2015 - 2024"
)

# Copy sang thư mục artifact nếu tồn tại
artifact_base = "/home/bush/.gemini/antigravity-cli/brain/913449d4-bd8f-41cd-9eb9-061295700ef9"
if os.path.exists(artifact_base):
    for period in ["period_2017_2026", "period_2015_2024"]:
        dest = os.path.join(artifact_base, period)
        os.makedirs(dest, exist_ok=True)
        charts_src = os.path.join(BASE_DIR, "charts", period)
        if os.path.exists(charts_src):
            for fname in os.listdir(charts_src):
                src_f = os.path.join(charts_src, fname)
                shutil.copy(src_f, dest)

print("Hoàn tất tạo biểu đồ và đồng bộ thư mục!")

