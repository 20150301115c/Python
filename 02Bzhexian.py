import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties
from io import BytesIO

# ===================== 核心：加载 SIMHEI.TTF 字体 =====================
# 加载本地黑体字体文件（必须与脚本同目录）
simhei = FontProperties(fname="./SIMHEI.TTF", size=24)
# 全局基础配置
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题
# =====================================================================

# -------------------------- Streamlit 页面配置 --------------------------
st.set_page_config(page_title="维度对比绘图工具", layout="wide")
st.title("📊 维度对比折线图（论文版）")
st.markdown("---")

# -------------------------- 侧边栏：维度数量设置 --------------------------
st.sidebar.header("⚙️ 基础设置")
dim_count = st.sidebar.slider("维度数量", min_value=1, max_value=10, value=5)

# -------------------------- 动态输入数据 --------------------------
st.subheader("📝 输入数据")
col1, col2, col3 = st.columns(3)

dim_names = []
group1 = []
group2 = []

for i in range(dim_count):
    with col1:
        name = st.text_input(f"维度 {i+1} 名称", value=f"维度{i+1}", key=f"name_{i}")
        dim_names.append(name)
    with col2:
        score1 = st.number_input(f"实验组 {i+1}", value=3.0, step=0.01, key=f"g1_{i}", format="%.2f")
        group1.append(score1)
    with col3:
        score2 = st.number_input(f"对照组 {i+1}", value=3.0, step=0.01, key=f"g2_{i}", format="%.2f")
        group2.append(score2)

st.markdown("---")

# -------------------------- 生成图表 --------------------------
if st.button("🚀 生成对比图", type="primary"):
    x = np.arange(1, dim_count + 1)
    fig, ax = plt.subplots(figsize=(16, 8))

    # 绘制折线（原版配色+样式）
    ax.plot(x, group1, 'o-', color='#E74C3C', linewidth=3, markersize=12, label='实验组')
    ax.plot(x, group2, 's--', color='#3498DB', linewidth=3, markersize=12, label='对照组')

    # X轴设置（强制黑体）
    ax.set_xticks(x)
    ax.set_xticklabels(dim_names, fontproperties=simhei)
    
    # 动态适配Y轴（自动计算范围）
    all_data = group1 + group2
    min_y = round(min(all_data) - 0.2, 1)
    max_y = round(max(all_data) + 0.2, 1)
    ax.set_ylim(min_y, max_y)

    # 所有文字强制使用 SIMHEI.TTF
    ax.set_ylabel('得分', fontproperties=simhei)
    ax.legend(prop=simhei, loc='upper right')
    ax.grid(True, alpha=0.3)

    # 布局优化
    plt.tight_layout()

    # 显示图表
    st.pyplot(fig)

    # 高清图片下载
    buf = BytesIO()
    plt.savefig(buf, dpi=300, bbox_inches='tight', format='png')
    buf.seek(0)
    st.download_button("📥 下载高清PNG", buf, "维度对比图.png", "image/png")

    plt.close()

st.markdown("---")
st.caption("✅ 基于 SIMHEI.TTF 黑体字体 | 自动适配Y轴 | 全局24号字体 | Streamlit Cloud 专用")
