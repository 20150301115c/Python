import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# -------------------------- 核心：加载 SIMHEI.TTF 字体 --------------------------
# 加载本地黑体字体（Streamlit Cloud 专用）
simhei = FontProperties(fname="./SIMHEI.TTF", size=20)
# 基础配置
plt.rcParams["axes.unicode_minus"] = False  # 负号正常显示
plt.rcParams['font.size'] = 20  # 全局字体大小20

# -------------------------- 页面基础配置 --------------------------
st.set_page_config(page_title="均值误差柱状图生成器", layout="wide")
st.title("📊 能力维度均值误差柱状图生成器")
st.markdown("---")

# -------------------------- 核心交互区域 --------------------------
st.sidebar.header("⚙️ 参数设置")

# 1. 选择维度数量（3-5维，和雷达图保持一致）
n_dims = st.sidebar.selectbox("选择维度数量", options=[3, 4, 5], index=2)

st.subheader("📝 第一步：设置维度名称")
dimensions = []
# 动态生成维度名称输入框
for i in range(n_dims):
    dim_name = st.text_input(f"维度 {i+1} 名称", value=f"维度{i+1}", key=f"dim_{i}")
    dimensions.append(dim_name)

st.markdown("---")
st.subheader("📝 第二步：输入各维度数据（均值+标准差）")

# 存储数据
means = []
stds = []

# 动态生成每个维度的输入框
for idx, dim in enumerate(dimensions):
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            mean_val = st.number_input(
                f"{dim} - 平均值",
                min_value=0.0, max_value=5.0, value=2.70, step=0.01,
                key=f"mean_{idx}"
            )
        with col2:
            std_val = st.number_input(
                f"{dim} - 标准差",
                min_value=0.0, max_value=2.0, value=0.80, step=0.0001,
                key=f"std_{idx}"
            )
        means.append(mean_val)
        stds.append(std_val)

st.markdown("---")

# -------------------------- 生成图表按钮 --------------------------
if st.button("🚀 生成柱状图", type="primary"):
    # 数据保留两位小数
    rounded_means = [round(m, 2) for m in means]
    rounded_stds = [round(s, 2) for s in stds]

    # 完全保留原版画布尺寸
    plt.figure(figsize=(10, 6))

    # 绘制带误差线的柱状图（原版参数不变）
    bars = plt.bar(
        dimensions, 
        rounded_means, 
        yerr=rounded_stds,
        capsize=5,
        width=0.3,
        color='#4682B4',
        edgecolor='black'
    )

    # 柱子上方数值标注（指定黑体）
    for bar, mean in zip(bars, rounded_means):
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.03,
            f'{mean:.2f}',
            ha='center', va='bottom', fontsize=20, fontproperties=simhei
        )

    # 图表样式（指定黑体，完全复刻原版）
    plt.ylabel('平均值', fontproperties=simhei)
    plt.ylim(0, 3.7)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    # X轴维度名称指定黑体
    plt.xticks(fontproperties=simhei)
    plt.tight_layout()

    # 在Streamlit中展示图表
    st.pyplot(plt.gcf())
    st.success("✅ 柱状图生成完成！中文黑体显示正常！")

    plt.close()
