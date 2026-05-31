import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
# 关键：导入字体加载工具
from matplotlib.font_manager import FontProperties

# ===================== 字体核心配置（固定不动）=====================
# 加载根目录下的 SIMHEI.TTF 字体，路径严格对应文件名
FONT_PATH = "./SIMHEI.TTF"
my_font = FontProperties(fname=FONT_PATH)

# 解决负号显示方块，仅此一行保留，其余字体别名全部删除
plt.rcParams["axes.unicode_minus"] = False

# ===================== 页面基础配置 =====================
st.set_page_config(page_title="能力提升雷达图生成器", layout="wide")
st.title("📊 能力提升幅度雷达图生成器")
st.markdown("---")

# ===================== 侧边栏参数设置 =====================
st.sidebar.header("⚙️ 基础参数设置")
n_groups = st.sidebar.selectbox("选择组别数量", options=[1, 2, 3, 4], index=3)
n_dims = st.sidebar.selectbox("选择维度数量", options=[3, 4, 5], index=2)

# 维度名称输入
st.subheader("📝 第一步：设置维度名称")
dimensions = []
for i in range(n_dims):
    dim_name = st.text_input(f"维度 {i+1} 名称", value=f"维度{i+1}", key=f"dim_{i}")
    dimensions.append(dim_name)

st.markdown("---")
st.subheader("📝 第二步：设置各组信息与数据")

# 组别默认样式
default_styles = [
    {'color': '#E74C3C', 'marker': 'o', 'label': '实验组A'},
    {'color': '#3498DB', 'marker': 's', 'label': '实验组B'},
    {'color': '#2ECC71', 'marker': '^', 'label': '对照组C'},
    {'color': '#F39C12', 'marker': 'd', 'label': '对照组D'},
]
marker_options = ["o", "s", "^", "d", "*", "p"]

class_styles = []
improve_data = []

# 动态录入每组配置+数据
for group_idx in range(n_groups):
    with st.expander(f"组别 {group_idx+1} 设置", expanded=True):
        label = st.text_input("组别名称", value=default_styles[group_idx]['label'], key=f"label_{group_idx}")
        color = st.color_picker("选择颜色", value=default_styles[group_idx]['color'], key=f"color_{group_idx}")
        marker = st.selectbox("选择标记样式", options=marker_options, 
                              index=marker_options.index(default_styles[group_idx]['marker']), 
                              key=f"marker_{group_idx}")

        st.markdown("**提升幅度数据**")
        group_data = []
        for dim_idx in range(n_dims):
            data = st.number_input(
                f"{dimensions[dim_idx]}",
                min_value=0.0, max_value=2.0, value=0.50, step=0.01,
                key=f"data_{group_idx}_{dim_idx}"
            )
            group_data.append(data)

        class_styles.append({'color': color, 'marker': marker, 'label': label})
        improve_data.append(group_data)

st.markdown("---")

# ===================== 生成雷达图 =====================
if st.button("🚀 生成雷达图", type="primary"):
    fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(polar=True))

    angles = np.linspace(0, 2 * np.pi, len(dimensions), endpoint=False).tolist()
    angles += angles[:1]

    # 【重点1：维度中文 → 绑定自定义字体】
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(dimensions, fontproperties=my_font, fontsize=18)

    ax.set_yticklabels([])
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    # 绘制各组曲线
    for idx in range(n_groups):
        values = improve_data[idx]
        values += values[:1]
        ax.plot(
            angles, values,
            color=class_styles[idx]['color'],
            marker=class_styles[idx]['marker'],
            markersize=8,
            linewidth=2,
            label=class_styles[idx]['label']
        )
        ax.fill(angles, values, color=class_styles[idx]['color'], alpha=0.1)

    # 【重点2：图例中文 → 绑定自定义字体】
    ax.legend(
        loc='upper right', 
        bbox_to_anchor=(1.3, 1.0), 
        framealpha=0.9, 
        prop=my_font,  # 图例用 prop=字体对象
        fontsize=16
    )

    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    st.pyplot(fig)
    st.success("✅ 雷达图生成完成！")
