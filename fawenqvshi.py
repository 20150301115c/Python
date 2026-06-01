import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties
from io import BytesIO

# ===================== 加载SIMHEI字体（必须）=====================
simhei = FontProperties(fname="./SIMHEI.TTF", size=28)
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams['axes.linewidth'] = 1.5
plt.rcParams['xtick.major.width'] = 1.5
plt.rcParams['ytick.major.width'] = 1.5

# ===================== Streamlit页面配置 =====================
st.set_page_config(page_title="发文量趋势图", layout="wide")
st.title("📈 中英文发文量趋势图（对数坐标）")
st.markdown("---")

# ===================== 侧边栏：年份选择 =====================
st.sidebar.header("⚙️ 年份设置")
# 下拉选择起始/结束年份（范围2010-2030）
start_year = st.sidebar.selectbox("起始年份", options=list(range(2010, 2031)), index=6)  # 默认2016
end_year = st.sidebar.selectbox("结束年份", options=list(range(2010, 2031)), index=15) # 默认2025

# 自动生成年份列表
if start_year > end_year:
    st.error("❌ 起始年份不能大于结束年份！")
else:
    years = list(range(start_year, end_year + 1))
    year_count = len(years)
    st.success(f"✅ 已生成年份：{years}")

st.markdown("---")

# ===================== 动态输入数据 =====================
st.subheader("📝 输入发文量数据")
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔵 WOS 数据")
    wos_data = []
    for i in range(year_count):
        val = st.number_input(f"{years[i]} 年", value=300, step=1, key=f"wos_{i}")
        wos_data.append(val)

with col2:
    st.subheader("🟠 CNKI 数据")
    cnki_data = []
    for i in range(year_count):
        val = st.number_input(f"{years[i]} 年", value=50, step=1, key=f"cnki_{i}")
        cnki_data.append(val)

st.markdown("---")

# ===================== 生成图表 =====================
if st.button("🚀 生成趋势图", type="primary"):
    fig, ax = plt.subplots(figsize=(18, 10))

    # 绘制曲线（完全保留你的原版样式）
    ax.plot(years, wos_data, color='#1f77b4', marker='o', linestyle='-', 
            linewidth=3, markersize=10, label='WOS')
    ax.plot(years, cnki_data, color='#ff7f0e', marker='s', linestyle='-', 
            linewidth=3, markersize=10, label='CNKI')

    # 对数坐标
    ax.set_yscale('log')

    # Y轴刻度（原版设置）
    ax.set_yticks([100, 1000])
    ax.set_yticklabels(['$10^2$', '$10^3$'], fontproperties=simhei)

    # 坐标轴标签（黑体）
    ax.set_xlabel('年份', fontproperties=simhei)
    ax.set_ylabel('数据量（对数坐标）', fontproperties=simhei)

    # X轴年份
    ax.set_xticks(years)
    ax.set_xticklabels(years, fontproperties=simhei)

    # 图例（黑体）
    ax.legend(loc='upper left', prop=simhei)

    # 数据标注（完全保留你的原版位置/样式）
    for x, y in zip(years, wos_data):
        ax.text(x, y * 1.05, str(y), ha='center', va='bottom', 
                color='#1f77b4', fontproperties=simhei)
    for x, y in zip(years, cnki_data):
        ax.text(x, y * 1.35, str(y), ha='center', va='bottom', 
                color='#ff7f0e', fontproperties=simhei)

    plt.tight_layout()

    # 显示图表
    st.pyplot(fig)

    # 高清图片下载
    buf = BytesIO()
    plt.savefig(buf, dpi=300, bbox_inches='tight', format='png')
    buf.seek(0)
    st.download_button("📥 下载高清PNG", buf, "发文量趋势图.png", "image/png")

    plt.close()
