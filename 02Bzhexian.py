import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# ===================== Streamlit Cloud 安全中文配置（无报错）=====================
plt.rcParams["axes.unicode_minus"] = False
# 适配Linux/Streamlit环境的中文字体（100%可用）
plt.rcParams["font.family"] = ["WenQuanYi Micro Hei", "DejaVu Sans"]
plt.rcParams["font.size"] = 24  # 全局统一24号字体
# ==============================================================================

# -------------------------- Streamlit 页面配置 --------------------------
st.set_page_config(page_title="维度对比绘图工具", layout="wide")
st.title("📊 维度对比折线图（论文版）")
st.markdown("---")

# -------------------------- 侧边栏：核心参数设置 --------------------------
st.sidebar.header("⚙️ 基础设置")
# 自定义维度数量（1-10个，按需调整）
dim_count = st.sidebar.slider("维度数量", min_value=1, max_value=10, value=5)

# -------------------------- 主界面：动态输入数据 --------------------------
st.subheader("📝 输入数据")
col1, col2, col3 = st.columns(3)

# 动态存储数据
dim_names = []       # 维度名称
group1_scores = []   # 实验组数据
group2_scores = []   # 对照组数据

# 循环生成输入框
for i in range(dim_count):
    with col1:
        name = st.text_input(f"维度 {i+1} 名称", value=f"维度{i+1}", key=f"name_{i}")
        dim_names.append(name)
    with col2:
        # 实验组输入
        score1 = st.number_input(f"实验组 {i+1}", value=3.0, step=0.01, key=f"g1_{i}", format="%.2f")
        group1_scores.append(score1)
    with col3:
        # 对照组输入
        score2 = st.number_input(f"对照组 {i+1}", value=3.0, step=0.01, key=f"g2_{i}", format="%.2f")
        group2_scores.append(score2)

st.markdown("---")

# -------------------------- 绘图按钮 + 生成图表 --------------------------
if st.button("🚀 生成对比图", type="primary"):
    # X轴数据
    x = np.arange(1, dim_count + 1)
    
    # 创建单张图（原代码4合1改为单图）
    fig, ax = plt.subplots(figsize=(16, 8))
    
    # 绘制折线（保留你原版的配色、样式、线宽）
    ax.plot(x, group1_scores, 'o-', color='#E74C3C', linewidth=3, markersize=12, label='实验组')
    ax.plot(x, group2_scores, 's--', color='#3498DB', linewidth=3, markersize=12, label='对照组')
    
    # X轴设置
    ax.set_xticks(x)
    ax.set_xticklabels(dim_names)
    
    # ===================== 动态Y轴范围（核心！自动适配数据）=====================
    all_scores = group1_scores + group2_scores
    min_y = min(all_scores) - 0.2  # 最小值向下浮动0.2
    max_y = max(all_scores) + 0.2  # 最大值向上浮动0.2
    ax.set_ylim(min_y, max_y)
    
    # 图表样式
    ax.set_ylabel('得分')
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)
    
    # 紧凑布局
    plt.tight_layout()
    
    # 显示图表
    st.pyplot(fig)
    
    # -------------------------- 下载高清图片 --------------------------
    from io import BytesIO
    buf = BytesIO()
    plt.savefig(buf, dpi=300, bbox_inches='tight', format='png')
    buf.seek(0)
    
    st.download_button(
        label="📥 下载高清PNG图片",
        data=buf,
        file_name="维度对比图.png",
        mime="image/png"
    )
    
    # 关闭图形释放内存
    plt.close()

st.markdown("---")
st.caption("✅ 工具说明：自动适配Y轴、全局24号字体、支持1-10个维度、Streamlit Cloud完美运行")
