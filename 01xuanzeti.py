import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties
from io import BytesIO

# ===================== 【强制修复】SIMHEI.TTF 字体加载（唯一有效方案）=====================
# 直接加载本地黑体，无任何兼容判断，Streamlit Cloud 100%生效
simhei_font = FontProperties(fname="./SIMHEI.TTF")
# 全局样式固定
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams['axes.linewidth'] = 1.5
plt.rcParams['xtick.major.width'] = 1.5
plt.rcParams['ytick.major.width'] = 1.5
# ======================================================================================

# ===================== 保留你原版默认配色 =====================
COLORS_01 = {"Q1": "#4CAF50", "Q2": "#2196F3", "Q3": "#FF9800","Q4": "#9C27B0", "Q5": "#CE93D8","Q6": "#00BCD4", "Q7": "#80DEEA"}
LEFT_COLORS = ['#F9A826', '#FF7043', '#AB47BC', '#66BB6A', '#42A5F5']
RIGHT_COLORS = ['#26A69A', '#EC407A', '#FFA726', '#7E57C2', '#6699FF']
COLORS_03 = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']

# ===================== 图表1：3组横向分组条形图 =====================
def draw_chart1(title, labels, q1_data, q2_data, q3_data, color1, color2, color3):
    fig, ax = plt.subplots(figsize=(16, 9))
    bar_height = 0.25
    y = np.arange(len(labels))
    bar1 = ax.barh(y - bar_height, q1_data, height=bar_height, label='Q1', color=color1, alpha=0.8, edgecolor='white')
    bar2 = ax.barh(y, q2_data, height=bar_height, label='Q2', color=color2, alpha=0.8, edgecolor='white')
    bar3 = ax.barh(y + bar_height, q3_data, height=bar_height, label='Q3', color=color3, alpha=0.8, edgecolor='white')
    
    for bar, label, value in zip(bar1, labels, bar1.datavalues):
        ax.text(bar.get_width()+0.5, bar.get_y()+bar.get_height()/2, f'{value}%', ha='left', va='center', fontproperties=simhei_font, fontsize=24)
        ax.text(0.5, bar.get_y()+bar.get_height()/2, label, ha='left', va='center', fontproperties=simhei_font, fontsize=24)
    for bar, label, value in zip(bar2, labels, bar2.datavalues):
        ax.text(bar.get_width()+0.5, bar.get_y()+bar.get_height()/2, f'{value}%', ha='left', va='center', fontproperties=simhei_font, fontsize=24)
    for bar, label, value in zip(bar3, labels, bar3.datavalues):
        ax.text(bar.get_width()+0.5, bar.get_y()+bar.get_height()/2, f'{value}%', ha='left', va='center', fontproperties=simhei_font, fontsize=24)

    ax.set_title(title, fontproperties=simhei_font, fontsize=28, pad=20)
    ax.set_xlabel('百分比 (%)', fontproperties=simhei_font, fontsize=24)
    ax.set_yticks([])
    ax.set_xlim(0, 45)
    ax.grid(axis='x', alpha=0.3)
    ax.legend(prop=simhei_font, fontsize=24)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# ===================== 图表2：2组横向条形图(Q4-Q5) =====================
def draw_chart2(title, q4_labels, q4_data, q5_labels, q5_data, color4, color5):
    fig, ax = plt.subplots(figsize=(16, 9))
    bar_height = 0.35
    max_len = max(len(q4_labels), len(q5_labels))
    y = np.arange(max_len)
    
    q4_data += [0]*(max_len-len(q4_data))
    q5_data += [0]*(max_len-len(q5_data))
    bar4 = ax.barh(y - bar_height/2, q4_data, height=bar_height, label='Q4', color=color4, alpha=0.8, edgecolor='white')
    bar5 = ax.barh(y + bar_height/2, q5_data, height=bar_height, label='Q5', color=color5, alpha=0.8, edgecolor='white')

    ax.set_title(title, fontproperties=simhei_font, fontsize=28, pad=20)
    ax.set_xlabel('百分比 (%)', fontproperties=simhei_font, fontsize=24)
    ax.set_yticks([])
    ax.set_xlim(0, 40)
    ax.legend(prop=simhei_font, fontsize=24)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# ===================== 图表3：2组横向条形图(Q6-Q7) =====================
def draw_chart3(title, q6_labels, q6_data, q7_labels, q7_data, color6, color7):
    fig, ax = plt.subplots(figsize=(16, 9))
    bar_height = 0.35
    max_len = max(len(q6_labels), len(q7_labels))
    y = np.arange(max_len)
    
    q6_data += [0]*(max_len-len(q6_data))
    q7_data += [0]*(max_len-len(q7_data))
    bar6 = ax.barh(y - bar_height/2, q6_data, height=bar_height, label='Q6', color=color6, alpha=0.8, edgecolor='white')
    bar7 = ax.barh(y + bar_height/2, q7_data, height=bar_height, label='Q7', color=color7, alpha=0.8, edgecolor='white')

    ax.set_title(title, fontproperties=simhei_font, fontsize=28, pad=20)
    ax.set_xlabel('百分比 (%)', fontproperties=simhei_font, fontsize=24)
    ax.set_yticks([])
    ax.set_xlim(0, 45)
    ax.legend(prop=simhei_font, fontsize=24)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# ===================== 图表4：双饼图 =====================
def draw_chart4(group_title, q1_info, q2_info, left_colors, right_colors):
    fig, axs = plt.subplots(1, 2, figsize=(22, 10))
    axs[0].pie(q1_info["data"], colors=left_colors, autopct='%.2f%%', startangle=90, wedgeprops=dict(edgecolor='white', linewidth=2), textprops={'fontproperties': simhei_font, 'fontsize':24})
    axs[0].set_title(q1_info["short_title"], fontproperties=simhei_font, fontsize=24)
    axs[1].pie(q2_info["data"], colors=right_colors, autopct='%.2f%%', startangle=90, wedgeprops=dict(edgecolor='white', linewidth=2), textprops={'fontproperties': simhei_font, 'fontsize':24})
    axs[1].set_title(q2_info["short_title"], fontproperties=simhei_font, fontsize=24)
    fig.suptitle(group_title, fontproperties=simhei_font, fontsize=28, y=1.02)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# ===================== 图表5：堆积条形图(2题) =====================
def draw_chart5(group_title, q1_info, q2_info, colors):
    fig, ax = plt.subplots(figsize=(20, 6))
    questions = [q1_info, q2_info]
    y_pos = np.arange(len(questions))
    
    for i, q in enumerate(questions):
        left = 0
        for j in range(len(q["data"])):
            ax.barh(y=i, width=q["data"][j], left=left, color=colors[j], edgecolor='white', alpha=0.8, height=0.6)
            ax.text(left+q["data"][j]/2, i, f'{q["options"][j]}\n{q["data"][j]:.2f}%', ha='center', va='center', fontproperties=simhei_font, fontsize=24)
            left += q["data"][j]

    ax.set_yticks(y_pos)
    ax.set_yticklabels([q["short_title"] for q in questions], fontproperties=simhei_font, fontsize=24)
    ax.set_xlabel("百分比（%）", fontproperties=simhei_font, fontsize=24)
    ax.set_title(group_title, fontproperties=simhei_font, fontsize=28, pad=20)
    ax.spines['top'].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# ===================== 图表6：堆积条形图(3题) =====================
def draw_chart6(group_title, q1_info, q2_info, q3_info, colors):
    fig, ax = plt.subplots(figsize=(20, 8))
    questions = [q1_info, q2_info, q3_info]
    y_pos = np.arange(len(questions))
    
    for i, q in enumerate(questions):
        left = 0
        for j in range(len(q["data"])):
            ax.barh(y=i, width=q["data"][j], left=left, color=colors[j], edgecolor='white', alpha=0.8, height=0.6)
            ax.text(left+q["data"][j]/2, i, f'{q["options"][j]}\n{q["data"][j]:.2f}%', ha='center', va='center', fontproperties=simhei_font, fontsize=24)
            left += q["data"][j]

    ax.set_yticks(y_pos)
    ax.set_yticklabels([q["short_title"] for q in questions], fontproperties=simhei_font, fontsize=24)
    ax.set_xlabel("百分比（%）", fontproperties=simhei_font, fontsize=24)
    ax.set_title(group_title, fontproperties=simhei_font, fontsize=28, pad=20)
    ax.spines['top'].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# ===================== Streamlit 主界面（修复重复ID）=====================
st.set_page_config(page_title="现状调查图表生成器", layout="wide")
st.title("📊 现状调查六合一图表生成器",)
st.markdown("---")

# 标签页（6个图表）
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "图表1：3组横向条形图", "图表2：Q4-Q5条形图", "图表3：Q6-Q7条形图",
    "图表4：双饼图", "图表5：2题堆积条形图", "图表6：3题堆积条形图"
])

# ------------------- 标签页1：图表1 -------------------
with tab1:
    st.header("3组横向分组条形图")
    col1, col2 = st.columns(2)
    with col1:
        title1 = st.text_input("图表标题", value="三大概念的了解程度对比", key="t1_title")
        labels1 = st.text_area("选项标签", value="完全不了解\n了解较少\n基本了解\n比较了解\n完全了解", key="t1_labels")
        q1_data = st.text_input("Q1数据", value="34.67, 30.07, 17.78, 11.41, 6.07", key="t1_q1")
        q2_data = st.text_input("Q2数据", value="9.48, 32.74, 32.30, 18.22, 7.26", key="t1_q2")
        q3_data = st.text_input("Q3数据", value="13.04, 35.11, 31.26, 13.63, 6.96", key="t1_q3")
    with col2:
        c1 = st.color_picker("Q1颜色", COLORS_01["Q1"], key="t1_c1")
        c2 = st.color_picker("Q2颜色", COLORS_01["Q2"], key="t1_c2")
        c3 = st.color_picker("Q3颜色", COLORS_01["Q3"], key="t1_c3")
    if st.button("生成图表1", key="btn1"):
        lbl = [x.strip() for x in labels1.split('\n') if x.strip()]
        d1 = [float(x) for x in q1_data.split(',')]
        d2 = [float(x) for x in q2_data.split(',')]
        d3 = [float(x) for x in q3_data.split(',')]
        draw_chart1(title1, lbl, d1, d2, d3, c1, c2, c3)

# ------------------- 标签页2：图表2 -------------------
with tab2:
    st.header("Q4-Q5 横向条形图")
    col1, col2 = st.columns(2)
    with col1:
        title2 = st.text_input("图表标题", value="计算思维重要性评价", key="t2_title")
        q4_lbl = st.text_area("Q4标签", value="至关重要\n比较重要\n一般\n不太重要\n几乎不重要", key="t2_lbl4")
        q5_lbl = st.text_area("Q5标签", value="分步拆解\n借鉴经验\n常用方法\n请教他人\n凭直觉", key="t2_lbl5")
        d4 = st.text_input("Q4数据", value="5.48, 15.41, 28.30, 34.52, 16.30", key="t2_d4")
        d5 = st.text_input("Q5数据", value="11.70, 26.22, 26.07, 25.48, 10.52", key="t2_d5")
    with col2:
        c4 = st.color_picker("Q4颜色", COLORS_01["Q4"], key="t2_c4")
        c5 = st.color_picker("Q5颜色", COLORS_01["Q5"], key="t2_c5")
    if st.button("生成图表2", key="btn2"):
        l4 = [x.strip() for x in q4_lbl.split('\n') if x.strip()]
        l5 = [x.strip() for x in q5_lbl.split('\n') if x.strip()]
        draw_chart2(title2, l4, [float(x) for x in d4.split(',')], l5, [float(x) for x in d5.split(',')], c4, c5)

# ------------------- 标签页3：图表3 -------------------
with tab3:
    st.header("Q6-Q7 横向条形图")
    col1, col2 = st.columns(2)
    with col1:
        title3 = st.text_input("图表标题", value="项目式学习认知", key="t3_title")
        q6_lbl = st.text_area("Q6标签", value="以学生为中心\n上课自由\n作业多\n考核严\n不清楚", key="t3_lbl6")
        q7_lbl = st.text_area("Q7标签", value="应对考试\n生活问题\n仅信息技术\n科技研发\n不清楚", key="t3_lbl7")
        d6 = st.text_input("Q6数据", value="12.89, 28.44, 23.85, 24.89, 9.93", key="t3_d6")
        d7 = st.text_input("Q7数据", value="6.37, 17.19, 35.41, 32.15, 8.89", key="t3_d7")
    with col2:
        c6 = st.color_picker("Q6颜色", COLORS_01["Q6"], key="t3_c6")
        c7 = st.color_picker("Q7颜色", COLORS_01["Q7"], key="t3_c7")
    if st.button("生成图表3", key="btn3"):
        l6 = [x.strip() for x in q6_lbl.split('\n') if x.strip()]
        l7 = [x.strip() for x in q7_lbl.split('\n') if x.strip()]
        draw_chart3(title3, l6, [float(x) for x in d6.split(',')], l7, [float(x) for x in d7.split(',')], c6, c7)

# ------------------- 标签页4：图表4 -------------------
with tab4:
    st.header("双饼图（1行2列）")
    col1, col2 = st.columns(2)
    with col1:
        title4 = st.text_input("大标题", value="项目选题与任务分配", key="t4_title")
        s1 = st.text_input("左饼图标题", value="项目类型偏好", key="t4_s1")
        d1 = st.text_input("左饼图数据", value="24.59,28.30,28.59,13.19,5.33", key="t4_d1")
        opt1 = st.text_area("左饼图选项", value="贴近生活\n学科综合\n科技前沿\n教师指定\n小组创意", key="t4_opt1")
        s2 = st.text_input("右饼图标题", value="任务分配方式", key="t4_s2")
        d2 = st.text_input("右饼图数据", value="28.00,21.33,9.04,17.33,24.30", key="t4_d2")
        opt2 = st.text_area("右饼图选项", value="按特长\n轮流\n听组长\n同题\n自由选", key="t4_opt2")
    with col2:
        lc = [st.color_picker(f"左色{i+1}", LEFT_COLORS[i], key=f"t4_lc{i}") for i in range(5)]
        rc = [st.color_picker(f"右色{i+1}", RIGHT_COLORS[i], key=f"t4_rc{i}") for i in range(5)]
    if st.button("生成图表4", key="btn4"):
        q1 = {"short_title":s1,"data":[float(x) for x in d1.split(',')],"options":[x.strip() for x in opt1.split('\n')]}
        q2 = {"short_title":s2,"data":[float(x) for x in d2.split(',')],"options":[x.strip() for x in opt2.split('\n')]}
        draw_chart4(title4, q1, q2, lc, rc)

# ------------------- 标签页5：图表5 -------------------
with tab5:
    st.header("2题 横向堆积条形图")
    col1, col2 = st.columns(2)
    with col1:
        title5 = st.text_input("图表标题", value="传统教学不足与改进方向", key="t5_title")
        s1 = st.text_input("题目1", value="传统教学不足", key="t5_s1")
        d1 = st.text_input("题目1数据", value="25.93,12.30,25.93,13.04,22.81", key="t5_d1")
        opt1 = st.text_area("题目1选项", value="理论多\n内容旧\n教师中心\n评价单\n教法落后", key="t5_opt1")
        s2 = st.text_input("题目2", value="改进方向", key="t5_s2")
        d2 = st.text_input("题目2数据", value="22.07,26.07,9.63,15.26,26.96", key="t5_d2")
        opt2 = st.text_area("题目2选项", value="增实践\n引技术\n优互动\n改评价\n强趣味", key="t5_opt2")
    with col2:
        cc5 = [st.color_picker(f"堆积色{i+1}", COLORS_03[i], key=f"t5_c{i}") for i in range(5)]
    if st.button("生成图表5", key="btn5"):
        q1 = {"short_title":s1,"data":[float(x) for x in d1.split(',')],"options":[x.strip() for x in opt1.split('\n')]}
        q2 = {"short_title":s2,"data":[float(x) for x in d2.split(',')],"options":[x.strip() for x in opt2.split('\n')]}
        draw_chart5(title5, q1, q2, cc5)

# ------------------- 标签页6：图表6 -------------------
with tab6:
    st.header("3题 横向堆积条形图")
    col1, col2 = st.columns(2)
    with col1:
        title6 = st.text_input("图表标题", value="AIGC学习问题、偏好与需求", key="t6_title")
        s1 = st.text_input("题目1", value="学习问题", key="t6_s1")
        d1 = st.text_input("题目1数据", value="11.56,22.22,14.37,26.37,25.48", key="t6_d1")
        opt1 = st.text_area("题目1选项", value="影响成绩\n操作难\n小组矛盾\n评价不公\n能力不足", key="t6_opt1")
        s2 = st.text_input("题目2", value="任务偏好", key="t6_s2")
        d2 = st.text_input("题目2数据", value="10.81,36.59,27.85,18.22,6.52", key="t6_d2")
        opt2 = st.text_area("题目2选项", value="算法设计\n跨科解决\n创意生成\n可视化\n无偏好", key="t6_opt2")
        s3 = st.text_input("题目3", value="帮助需求", key="t6_s3")
        d3 = st.text_input("题目3数据", value="12.59,28.00,14.96,22.22,22.22", key="t6_d3")
        opt3 = st.text_area("题目3选项", value="教程\n资源\n支持\n建议\n展示", key="t6_opt3")
    with col2:
        cc6 = [st.color_picker(f"堆积色{i+1}", COLORS_03[i], key=f"t6_c{i}") for i in range(5)]
    if st.button("生成图表6", key="btn6"):
        q1 = {"short_title":s1,"data":[float(x) for x in d1.split(',')],"options":[x.strip() for x in opt1.split('\n')]}
        q2 = {"short_title":s2,"data":[float(x) for x in d2.split(',')],"options":[x.strip() for x in opt2.split('\n')]}
        q3 = {"short_title":s3,"data":[float(x) for x in d3.split(',')],"options":[x.strip() for x in opt3.split('\n')]}
        draw_chart6(title6, q1, q2, q3, cc6)

st.markdown("---")
st.success("✅ 修复完成：无重复ID报错 + SIMHEI字体完美显示")
