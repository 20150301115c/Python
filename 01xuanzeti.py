import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties

# ===================== 【强制SIMHEI字体】=====================
simhei_font = FontProperties(fname="./SIMHEI.TTF")
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams['axes.linewidth'] = 1.5
plt.rcParams['xtick.major.width'] = 1.5
plt.rcParams['ytick.major.width'] = 1.5

# 原有配色
COLORS_01 = {"Q1": "#4CAF50", "Q2": "#2196F3", "Q3": "#FF9800","Q4": "#9C27B0", "Q5": "#CE93D8","Q6": "#00BCD4", "Q7": "#80DEEA"}
LEFT_COLORS = ['#F9A826', '#FF7043', '#AB47BC', '#66BB6A', '#42A5F5']
RIGHT_COLORS = ['#26A69A', '#EC407A', '#FFA726', '#7E57C2', '#6699FF']
COLORS_03 = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
# 量表默认5色
SCALE_COLOR = ['#E74C3C','#E67E22','#F1C40F','#2ECC71','#3498DB']

# ====================原有6个绘图函数保留====================
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
    ax.grid(axis='x', alpha=0.3)
    ax.legend(prop=simhei_font, fontsize=24)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

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
    ax.grid(axis='x', alpha=0.3)
    ax.legend(prop=simhei_font, fontsize=24)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

def draw_chart4(group_title, q1_info, q2_info, left_colors, right_colors):
    fig, axs = plt.subplots(1, 2, figsize=(22, 10))
    axs[0].pie(q1_info["data"], colors=left_colors, autopct='%.2f%%', startangle=90, wedgeprops=dict(edgecolor='white', linewidth=2), textprops={'fontproperties':simhei_font,'fontsize':24})
    axs[0].set_title(q1_info["short_title"], fontproperties=simhei_font, fontsize=24)
    axs[1].pie(q2_info["data"], colors=right_colors, autopct='%.2f%%', startangle=90, wedgeprops=dict(edgecolor='white', linewidth=2), textprops={'fontproperties':simhei_font,'fontsize':24})
    axs[1].set_title(q2_info["short_title"], fontproperties=simhei_font, fontsize=24)
    fig.suptitle(group_title, fontproperties=simhei_font, fontsize=28, y=1.02)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

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
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

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
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# =====================【新增：第7个绘图函数：量表横向堆叠条形】=====================
def draw_chart7(fig_title, item_names, option_names, color_list, all_data):
    """
    item_names: 题目列表
    option_names:5个选项
    all_data:[[5个数值],...] 每题5个百分比
    """
    fig, ax = plt.subplots(figsize=(20, 2+len(item_names)*1.1))
    y_pos = np.arange(len(item_names))
    for idx, data_row in enumerate(all_data):
        left = 0
        for opt_idx, val in enumerate(data_row):
            ax.barh(y=idx, width=val, left=left, color=color_list[opt_idx], edgecolor='white', alpha=0.8, height=0.6)
            ax.text(left + val/2, idx, f'{option_names[opt_idx]}\n{val:.2f}%', ha='center', va='center', fontproperties=simhei_font, fontsize=22)
            left += val
    ax.set_yticks(y_pos)
    ax.set_yticklabels(item_names, fontproperties=simhei_font, fontsize=22)
    ax.set_xlabel("百分比（%）", fontproperties=simhei_font, fontsize=24)
    ax.set_title(fig_title, fontproperties=simhei_font, fontsize=28, pad=20)
    ax.set_xlim(0,105)
    ax.set_xticks([0,20,40,60,80,100])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# =====================页面主体=====================
st.set_page_config(page_title="现状调查六合一+量表", layout="wide")
st.title("📊 现状调查+量表图表生成器")
st.markdown("---")

# 7个标签！
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "图表1：3组横向条形",
    "图表2：Q4-Q5条形",
    "图表3：Q6-Q7条形",
    "图表4：双饼图",
    "图表5：2题堆积",
    "图表6：3题堆积",
    "图表7：量表题(1~6题)"
])

# ==========tab1~tab6原有代码不变（key全部保留）=========
#tab1
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
#tab2
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
#tab3
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
#tab4
with tab4:
    st.header("双饼图（1行2列）")
    col1, col2 = st.columns(2)
    with col1:
        title4 = st.text_input("大标题", value="项目选题与任务分配", key="t4_title")
        s1 = st.text_input("左饼标题", value="项目类型偏好", key="t4_s1")
        d1 = st.text_input("左数据", value="24.59,28.30,28.59,13.19,5.33", key="t4_d1")
        opt1 = st.text_area("左选项", value="贴近生活\n学科综合\n科技前沿\n教师指定\n小组创意", key="t4_opt1")
        s2 = st.text_input("右饼标题", value="任务分配方式", key="t4_s2")
        d2 = st.text_input("右数据", value="28.00,21.33,9.04,17.33,24.30", key="t4_d2")
        opt2 = st.text_area("右选项", value="按特长\n轮流\n听组长\n全员同题\n自由选", key="t4_opt2")
    with col2:
        lc = [st.color_picker(f"左{i+1}",LEFT_COLORS[i],key=f"t4_lc{i}") for i in range(5)]
        rc = [st.color_picker(f"右{i+1}",RIGHT_COLORS[i],key=f"t4_rc{i}")]
    if st.button("生成图表4", key="btn4"):
        q1={"short_title":s,"data":[float(x) for x in d1.split(',')],"options":[x.strip() for x in opt1.split('\n')]}
        q1={"short_title":s1,"data":[float(x) for x in d1.split(',')],"options":[x.strip() for x in opt1.split('\n')]}
        q2={"short_title":s2,"data":[float(x) for x in d2.split(',')],"options":[x.strip() for x in opt2.split('\n')]}
        draw_chart4(title4,q1,q2,lc,rc)
#tab5
with tab5:
    st.header("2题横向堆积")
    col1, col2 = st.columns(2)
    with col1:
        title5 = st.text_input("标题",value="传统课堂不足与改进",key="t5_title")
        s1=st.text_input("题1名称",value="题18：传统教学不足",key="t5_s1")
        d1=st.text_input("题1数据",value="25.93,12.30,25.93,13.04,22.81",key="t5_d1")
        o1=st.text_area("题1选项",value="理论多实践少\n内容陈旧\n教师中心\n评价单一\n教法落后",key="t5_o1")
        s2=st.text_input("题2名称",value="题19：项目改进方向",key="t5_s2")
        d2=st.text_input("题2数据",value="22.07,26.07,9.63,15.26,26.96",key="t5_d2")
        o2=st.text_area("题2选项",value="增实践\n引前沿\n优互动\n改考核\n强趣味",key="t5_o2")
    with col2:
        c5=[st.color_picker(f"色{i+1}",COLORS_03[i],key=f"t5_c{i}") for i in range(5)]
    if st.button("生成图表5",key="btn5"):
        q1={"short_title":s1,"data":[float(x) for x in d1.split(',')],"options":[x.strip() for x in o1.split('\n')]}
        q2={"short_title":s2,"data":[float(x) for x in d2.split(',')],"options":[x.strip() for x in o2.split('\n')]}
        draw_chart5(title5,q1,q2,c5)
#tab6
with tab6:
    st.header("3题横向堆积")
    col1, col2 = st.columns(2)
    with col1:
        title6=st.text_input("标题",value="AIGC相关调查",key="t6_title")
        s20=st.text_input("题1",value="题20：AIGC学习问题",key="t6_s20")
        d20=st.text_input("数据",value="11.56,22.22,14.37,26.37,25.48",key="t6_d20")
        o20=st.text_area("选项",value="影响成绩\n操作复杂\n小组矛盾\n评价不公\n能力不足",key="t6_o20")
        s21=st.text_input("题2",value="题21：任务偏好",key="t6_s21")
        d21=st.text_input("数据",value="10.81,36.59,27.85,18.22,6.52",key="t6_d21")
        o21=st.text_area("选项",value="算法设计\n跨科\n创意\n可视化\n无偏好",key="t6_o21")
        s22=st.text_input("题3",value="题22：帮助需求",key="t6_s22")
        d22=st.text_input("数据",value="12.59,28.00,14.96,22.22,22.22",key="t6_d22")
        o22=st.text_area("选项",value="教程\n资源\n技术\n建议\n展示",key="t6_o22")
    with col2:
        c6=[st.color_picker(f"色{i+1}",COLORS_03[i],key=f"t6_c{i}") for i in range(5)]
    if st.button("生成图表6",key="btn6"):
        q1={"short_title":s20,"data":[float(x) for x in d20.split(',')],"options":[x.strip() for x in o20.split('\n')]}
        q2={"short_title":s21,"data":[float(x) for x in d21.split(',')],"options":[x.strip() for x in o21.split('\n')]}
        q3={"short_title":s22,"data":[float(x) for x in d22.split('\n')],"options":[x.strip() for x in o22.split('\n')]}
        draw_chart6(title6,q1,q2,q3,c6)

# =====================【新增tab7：量表】=====================
with tab7:
    st.header("📋 量表题横向堆积图（题目1~6自选，默认5等级选项）")
    col_left, col_right = st.columns([3,1])
    with col_left:
        fig_title = st.text_input("图表总标题",value="量表调查结果统计",key="t7_figtitle")
        qty = st.selectbox("选择题目数量",options=[1,2,3,4,5,6],index=4,key="t7_qty")
        st.subheader("修改5个选项名称（默认：完全不符合/比较不符合/符合/比较符合/完全符合）")
        opt_list = []
        default_opt = ["完全不符合","比较不符合","符合","比较符合","完全符合"]
        for i in range(5):
            txt = st.text_input(f"选项{i+1}",value=default_opt[i],key=f"t7_opt{i}")
            opt_list.append(txt)
        st.divider()
        item_names = []
        all_data = []
        for qn in range(qty):
            st.subheader(f"第{qn+1}题设置")
            q_name = st.text_input(f"题目名称",value=f"量表题目{qn+1}",key=f"t7_qname{qn}")
            data_str = st.text_input(f"5个百分比（逗号分隔）",value="20.0,20.0,20.0,20.0,20.0",key=f"t7_qdata{qn}")
            item_names.append(q_name.strip())
            row_data = [float(i.strip()) for i in data_str.split(",")]
            all_data.append(row_data)
    with col_right:
        st.subheader("5个选项配色")
        scale_color_set = []
        for i in range(5):
            c = st.color_picker(f"颜色{i+1}",SCALE_COLOR[i],key=f"t7_c{i}")
            scale_color_set.append(c)
    if st.button("生成量表图表",key="btn7",type="primary"):
        draw_chart7(fig_title,item_names,opt_list,scale_color_set,all)

st.markdown("---")
st.info("提示：SIMHEI.TTF放根目录，量表默认5个等级，题目1~6自由增减，选项可自定义修改")
