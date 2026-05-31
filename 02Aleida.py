import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# -------------------------- 页面基础配置 --------------------------
st.set_page_config(page_title="能力提升雷达图生成器", layout="wide")
st.title("📊 能力提升幅度雷达图生成器")
st.markdown("---")

# -------------------------- 全局中文显示配置 --------------------------
plt.rcParams["font.family"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# -------------------------- 核心交互区域 --------------------------
st.sidebar.header("⚙️ 基础参数设置")

# 1. 选择组数（1-4组）
n_groups = st.sidebar.selectbox("选择组别数量", options=[1, 2, 3, 4], index=3)

# 2. 选择维度数量（3-5维）
n_dims = st.sidebar.selectbox("选择维度数量", options=[3, 4, 5], index=2)

st.subheader("📝 第一步：设置维度名称")
dimensions = []
# 动态生成维度名称输入框
for i in range(n_dims):
    dim_name = st.text_input(f"维度 {i+1} 名称", value=f"维度{i+1}", key=f"dim_{i}")
    dimensions.append(dim_name)

st.markdown("---")
st.subheader("📝 第二步：设置各组信息与数据")

# 预设样式（兼容1-4组）
default_styles = [
    {'color': '#E74C3C', 'marker': 'o', 'label': '实验组A'},
    {'color': '#3498DB', 'marker': 's', 'label': '实验组B'},
    {'color': '#2ECC71', 'marker': '^', 'label': '对照组C'},
    {'color': '#F39C12', 'marker': 'd', 'label': '对照组D'},
]
marker_options = ["o", "s", "^", "d", "*", "p"]  # 常用标记样式

# 存储各组配置和数据
class_styles = []
improve_data = []

# 动态生成每组的配置输入
for group_idx in range(n_groups):
    with st.expander(f"组别 {group_idx+1} 设置", expanded=True):
        # 组名
        label = st.text_input("组别名称", value=default_styles[group_idx]['label'], key=f"label_{group_idx}")
        # 颜色选择
        color = st.color_picker("选择颜色", value=default_styles[group_idx]['color'], key=f"color_{group_idx}")
        # 标记样式
        marker = st.selectbox("选择标记样式", options=marker_options, index=marker_options.index(default_styles[group_idx]['marker']), key=f"marker_{group_idx}")
        
        # 输入该组各维度的提升数据
        st.markdown("**提升幅度数据**")
        group_data = []
        for dim_idx in range(n_dims):
            data = st.number_input(
                f"{dimensions[dim_idx]}",
                min_value=0.0, max_value=2.0, value=0.50, step=0.01,
                key=f"data_{group_idx}_{dim_idx}"
            )
            group_data.append(data)
        
        # 保存配置和数据
        class_styles.append({'color': color, 'marker': marker, 'label': label})
        improve_data.append(group_data)

st.markdown("---")

# -------------------------- 生成图表按钮 --------------------------
if st.button("🚀 生成雷达图", type="primary"):
    # -------------------------- 绘制雷达图 --------------------------
    fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(polar=True))

    # 计算雷达图角度
    angles = np.linspace(0, 2 * np.pi, len(dimensions), endpoint=False).tolist()
    angles += angles[:1]  # 闭合图形

    # 坐标轴配置
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(dimensions, fontsize=18)
    ax.set_yticklabels([])  # 隐藏径向刻度
    ax.set_theta_offset(np.pi / 2)  # 第一个维度置顶
    ax.set_theta_direction(-1)      # 顺时针排列

    # 绘制每组数据
    for idx in range(n_groups):
        values = improve_data[idx]
        values += values[:1]  # 闭合数值
        # 绘制折线
        ax.plot(
            angles, values,
            color=class_styles[idx]['color'],
            marker=class_styles[idx]['marker'],
            markersize=8,
            linewidth=2,
            label=class_styles[idx]['label']
        )
        # 填充半透明底色
        ax.fill(angles, values, color=class_styles[idx]['color'], alpha=0.1)

    # 图例与网格
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0), framealpha=0.9, fontsize=16)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    # 在Streamlit中展示图表
    st.pyplot(fig)

    st.success("✅ 雷达图生成完成！")