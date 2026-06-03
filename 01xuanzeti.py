import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
import os

# ===================== 核心配置：字体 + 全局样式 =====================
# 配置SimHei字体（解决中文显示问题）
def setup_font():
    # 方式1：加载系统SimHei字体（优先）
    try:
        font_path = font_manager.findfont("SimHei")
        if not font_path:
            # 方式2：如果系统无，则使用指定路径（需将SIMHEI.TTF放在同目录）
            font_path = "SIMHEI.TTF"
            if os.path.exists(font_path):
                font_prop = font_manager.FontProperties(fname=font_path)
                font_manager.fontManager.addfont(font_path)
                plt.rcParams['font.family'] = font_prop.get_name()
            else:
                st.warning("未找到SIMHEI.TTF字体文件，将使用备选中文字体")
                plt.rcParams["font.family"] = ["WenQuanYi Micro Hei", "DejaVu Sans"]
        else:
            plt.rcParams["font.family"] = ["SimHei"]
    except:
        plt.rcParams["font.family"] = ["WenQuanYi Micro Hei", "DejaVu Sans"]
    
    # 全局样式统一
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['font.size'] = 24
    plt.rcParams['axes.labelpad'] = 10
    plt.rcParams['axes.linewidth'] = 1.2
    plt.rcParams['legend.frameon'] = True
    plt.rcParams['legend.framealpha'] = 0.9

setup_font()

# ===================== 保留原代码默认配色 =====================
# 01文件默认配色
COLORS_01 = {
    "Q1": "#4CAF50", "Q2": "#2196F3", "Q3": "#FF9800",
    "Q4": "#9C27B0", "Q5": "#CE93D8",
    "Q6": "#00BCD4", "Q7": "#80DEEA"
}
# 02文件默认配色
LEFT_COLORS = ['#F9A826', '#FF7043', '#AB47BC', '#66BB6A', '#42A5F5']
RIGHT_COLORS = ['#26A69A', '#EC407A', '#FFA726', '#7E57C2', '#6699FF']
# 03文件默认配色
COLORS_03 = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']

# ===================== 图表1：Q1-Q3 横向分组条形图（3组） =====================
def draw_chart1(title, labels, q1_data, q2_data, q3_data, 
               color1=COLORS_01["Q1"], color2=COLORS_01["Q2"], color3=COLORS_01["Q3"]):
    fig, ax = plt.subplots(figsize=(16, 9))
    bar_height = 0.25
    y = np.arange(len(labels))

    # 绘制横向条形图
    bar1 = ax.barh(y - bar_height, q1_data, height=bar_height, label='Q1', color=color1, alpha=0.8, edgecolor='white', linewidth=1)
    bar2 = ax.barh(y, q2_data, height=bar_height, label='Q2', color=color2, alpha=0.8, edgecolor='white', linewidth=1)
    bar3 = ax.barh(y + bar_height, q3_data, height=bar_height, label='Q3', color=color3, alpha=0.8, edgecolor='white', linewidth=1)

    # 添加数值和标签
    def add_text(bars, labels, ax):
        for bar, label, value in zip(bars, labels, bars.datavalues):
            x_pos = bar.get_width() + 0.5 if value < 10 else bar.get_width() + 0.8
            ax.text(x_pos, bar.get_y() + bar.get_height()/2.,
                    f'{value}%', ha='left', va='center',
                    fontsize=24, fontweight='bold', color='black')
            ax.text(0.5, bar.get_y() + bar.get_height()/2.,
                    label, ha='left', va='center',
                    fontsize=24, color='#333333')

    add_text(bar1, labels, ax)
    add_text(bar2, labels, ax)
    add_text(bar3, labels, ax)

    # 样式设置
    ax.set_title(title, pad=20, fontweight='bold')
    ax.set_xlabel('百分比 (%)', fontweight='bold', labelpad=15)
    ax.set_ylabel('')
    ax.set_yticks([])
    ax.set_xlim(0, 45)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.legend(loc='upper right', bbox_to_anchor=(1, 0.95), fontsize=24)

    plt.tight_layout()
    st.pyplot(fig)

# ===================== 图表2：Q4-Q5 横向分组条形图（2组） =====================
def draw_chart2(title, q4_labels, q4_data, q5_labels, q5_data,
               color4=COLORS_01["Q4"], color5=COLORS_01["Q5"]):
    fig, ax = plt.subplots(figsize=(16, 9))
    bar_height = 0.35
    y = np.arange(max(len(q4_labels), len(q5_labels)))

    # 对齐标签长度
    max_len = max(len(q4_labels), len(q5_labels))
    q4_labels_pad = q4_labels + [""]*(max_len - len(q4_labels))
    q5_labels_pad = q5_labels + [""]*(max_len - len(q5_labels))
    q4_data_pad = q4_data + [0]*(max_len - len(q4_data))
    q5_data_pad = q5_data + [0]*(max_len - len(q5_data))

    # 绘制条形图
    bar4 = ax.barh(y - bar_height/2, q4_data_pad, height=bar_height, label='Q4', color=color4, alpha=0.8, edgecolor='white', linewidth=1)
    bar5 = ax.barh(y + bar_height/2, q5_data_pad, height=bar_height, label='Q5', color=color5, alpha=0.8, edgecolor='white', linewidth=1)

    # 添加数值和标签
    def add_text(bars, labels, ax):
        for bar, label, value in zip(bars, labels, bars.datavalues):
            if value == 0:
                continue
            x_pos = bar.get_width() + 0.5 if value < 10 else bar.get_width() + 0.8
            ax.text(x_pos, bar.get_y() + bar.get_height()/2.,
                    f'{value}%', ha='left', va='center',
                    fontsize=24, fontweight='bold', color='black')
            ax.text(0.5, bar.get_y() + bar.get_height()/2.,
                    label, ha='left', va='center',
                    fontsize=24, color='#333333')

    add_text(bar4, q4_labels_pad, ax)
    add_text(bar5, q5_labels_pad, ax)

    # 样式设置
    ax.set_title(title, pad=20, fontweight='bold')
    ax.set_xlabel('百分比 (%)', fontweight='bold', labelpad=15)
    ax.set_ylabel('')
    ax.set_yticks([])
    ax.set_xlim(0, 40)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.legend(loc='upper right', bbox_to_anchor=(1, 0.95), fontsize=24)

    plt.tight_layout()
    st.pyplot(fig)

# ===================== 图表3：Q6-Q7 横向分组条形图（2组） =====================
def draw_chart3(title, q6_labels, q6_data, q7_labels, q7_data,
               color6=COLORS_01["Q6"], color7=COLORS_01["Q7"]):
    fig, ax = plt.subplots(figsize=(16, 9))
    bar_height = 0.35
    y = np.arange(max(len(q6_labels), len(q7_labels)))

    # 对齐标签长度
    max_len = max(len(q6_labels), len(q7_labels))
    q6_labels_pad = q6_labels + [""]*(max_len - len(q6_labels))
    q7_labels_pad = q7_labels + [""]*(max_len - len(q7_labels))
    q6_data_pad = q6_data + [0]*(max_len - len(q6_data))
    q7_data_pad = q7_data + [0]*(max_len - len(q7_data))

    # 绘制条形图
    bar6 = ax.barh(y - bar_height/2, q6_data_pad, height=bar_height, label='Q6', color=color6, alpha=0.8, edgecolor='white', linewidth=1)
    bar7 = ax.barh(y + bar_height/2, q7_data_pad, height=bar_height, label='Q7', color=color7, alpha=0.8, edgecolor='white', linewidth=1)

    # 添加数值和标签
    def add_text(bars, labels, ax):
        for bar, label, value in zip(bars, labels, bars.datavalues):
            if value == 0:
                continue
            x_pos = bar.get_width() + 0.5 if value < 10 else bar.get_width() + 0.8
            ax.text(x_pos, bar.get_y() + bar.get_height()/2.,
                    f'{value}%', ha='left', va='center',
                    fontsize=24, fontweight='bold', color='black')
            ax.text(0.5, bar.get_y() + bar.get_height()/2.,
                    label, ha='left', va='center',
                    fontsize=24, color='#333333')

    add_text(bar6, q6_labels_pad, ax)
    add_text(bar7, q7_labels_pad, ax)

    # 样式设置
    ax.set_title(title, pad=20, fontweight='bold')
    ax.set_xlabel('百分比 (%)', fontweight='bold', labelpad=15)
    ax.set_ylabel('')
    ax.set_yticks([])
    ax.set_xlim(0, 45)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.legend(loc='upper right', bbox_to_anchor=(1, 0.95), fontsize=24)

    plt.tight_layout()
    st.pyplot(fig)

# ===================== 图表4：双饼图（1行2列） =====================
def draw_chart4(group_title, q1_info, q2_info, 
               left_colors=LEFT_COLORS, right_colors=RIGHT_COLORS, figsize=(22, 10)):
    fig, axs = plt.subplots(1, 2, figsize=figsize)
    
    # 绘制第一个饼图
    ax1 = axs[0]
    wedges1, texts1, autotexts1 = ax1.pie(
        q1_info["data"],
        colors=left_colors,
        autopct='%.2f%%',
        startangle=90,
        wedgeprops=dict(edgecolor='white', linewidth=2, alpha=0.8),
        textprops=dict(fontsize=24, fontweight='bold')
    )
    ax1.legend(wedges1, q1_info["options"], title="选项", loc="upper right", 
              fontsize=24, title_fontsize=16, bbox_to_anchor=(1.2, 1))
    ax1.set_title(q1_info["short_title"], fontsize=24, fontweight='bold', pad=15)

    # 绘制第二个饼图
    ax2 = axs[1]
    wedges2, texts2, autotexts2 = ax2.pie(
        q2_info["data"],
        colors=right_colors,
        autopct='%.2f%%',
        startangle=90,
        wedgeprops=dict(edgecolor='white', linewidth=2, alpha=0.8),
        textprops=dict(fontsize=24, fontweight='bold')
    )
    ax2.legend(wedges2, q2_info["options"], title="选项", loc="upper right", 
              fontsize=24, title_fontsize=16, bbox_to_anchor=(1.2, 1))
    ax2.set_title(q2_info["short_title"], fontsize=24, fontweight='bold', pad=15)

    # 全局样式
    fig.suptitle(group_title, fontsize=24, fontweight='bold', y=1.02)
    plt.tight_layout()
    st.pyplot(fig)

# ===================== 图表5：横向堆积条形图（2题） =====================
def draw_chart5(group_title, q1_info, q2_info, colors=COLORS_03, figsize=(20, 6)):
    fig, ax = plt.subplots(figsize=figsize)
    questions = [q1_info, q2_info]
    y_pos = np.arange(len(questions))

    for i, q in enumerate(questions):
        data = q["data"]
        options = q["options"]
        left = 0
        for j in range(len(data)):
            ax.barh(
                y=i, width=data[j], left=left,
                color=colors[j], edgecolor='white', alpha=0.8, height=0.6
            )
            # 添加标签
            label_text = f"{options[j]}\n{data[j]:.2f}%"
            ax.text(
                x=left + data[j]/2, y=i, s=label_text,
                ha='center', va='center', fontsize=24, fontweight='bold'
            )
            left += data[j]

    # 样式设置
    ax.set_yticks(y_pos)
    ax.set_yticklabels([q["short_title"] for q in questions], fontweight='bold')
    ax.set_xlim(0, 105)
    ax.set_xticks(np.arange(0, 101, 20))
    ax.set_xlabel("百分比（%）", fontweight='bold', fontsize=24)
    ax.set_title(group_title, fontsize=24, fontweight='bold', pad=20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    st.pyplot(fig)

# ===================== 图表6：横向堆积条形图（3题） =====================
def draw_chart6(group_title, q1_info, q2_info, q3_info, colors=COLORS_03, figsize=(20, 8)):
    fig, ax = plt.subplots(figsize=figsize)
    questions = [q1_info, q2_info, q3_info]
    y_pos = np.arange(len(questions))

    for i, q in enumerate(questions):
        data = q["data"]
        options = q["options"]
        left = 0
        for j in range(len(data)):
            ax.barh(
                y=i, width=data[j], left=left,
                color=colors[j], edgecolor='white', alpha=0.8, height=0.6
            )
            # 添加标签
            label_text = f"{options[j]}\n{data[j]:.2f}%"
            ax.text(
                x=left + data[j]/2, y=i, s=label_text,
                ha='center', va='center', fontsize=24, fontweight='bold'
            )
            left += data[j]

    # 样式设置
    ax.set_yticks(y_pos)
    ax.set_yticklabels([q["short_title"] for q in questions], fontweight='bold')
    ax.set_xlim(0, 105)
    ax.set_xticks(np.arange(0, 101, 20))
    ax.set_xlabel("百分比（%）", fontweight='bold', fontsize=24)
    ax.set_title(group_title, fontsize=24, fontweight='bold', pad=20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    st.pyplot(fig)

# ===================== Streamlit 界面布局 =====================
st.set_page_config(page_title="现状调查图表生成器", layout="wide")
st.title("现状调查多类型图表生成器")
st.markdown("---")

# 分标签页管理六种图表
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "图表1：3组横向条形图（Q1-Q3）",
    "图表2：2组横向条形图（Q4-Q5）",
    "图表3：2组横向条形图（Q6-Q7）",
    "图表4：双饼图（1行2列）",
    "图表5：堆积条形图（2题）",
    "图表6：堆积条形图（3题）"
])

# ===================== 标签页1：图表1 =====================
with tab1:
    st.header("3组横向分组条形图配置")
    col1, col2 = st.columns(2)
    
    with col1:
        title1 = st.text_input("图表标题", value="三大概念的了解程度对比（Q1-Q3）")
        labels1 = st.text_area("选项标签（每行一个）", value="完全不了解\n了解较少\n基本了解\n比较了解\n完全了解")
        q1_data_str = st.text_input("Q1数据（逗号分隔）", value="34.67, 30.07, 17.78, 11.41, 6.07")
        q2_data_str = st.text_input("Q2数据（逗号分隔）", value="9.48, 32.74, 32.30, 18.22, 7.26")
        q3_data_str = st.text_input("Q3数据（逗号分隔）", value="13.04, 35.11, 31.26, 13.63, 6.96")
    
    with col2:
        color1 = st.color_picker("Q1颜色", value=COLORS_01["Q1"])
        color2 = st.color_picker("Q2颜色", value=COLORS_01["Q2"])
        color3 = st.color_picker("Q3颜色", value=COLORS_01["Q3"])
    
    if st.button("生成图表1"):
        try:
            # 数据转换
            labels_list = [label.strip() for label in labels1.split('\n') if label.strip()]
            q1_data = [float(x.strip()) for x in q1_data_str.split(',')]
            q2_data = [float(x.strip()) for x in q2_data_str.split(',')]
            q3_data = [float(x.strip()) for x in q3_data_str.split(',')]
            
            # 校验长度
            max_len = max(len(labels_list), len(q1_data), len(q2_data), len(q3_data))
            if len(labels_list) < max_len:
                labels_list += [f"选项{i+1}" for i in range(len(labels_list), max_len)]
            q1_data += [0]*(max_len - len(q1_data))
            q2_data += [0]*(max_len - len(q2_data))
            q3_data += [0]*(max_len - len(q3_data))
            
            draw_chart1(title1, labels_list, q1_data, q2_data, q3_data, color1, color2, color3)
        except Exception as e:
            st.error(f"生成失败：{str(e)}")

# ===================== 标签页2：图表2 =====================
with tab2:
    st.header("2组横向分组条形图配置（Q4-Q5）")
    col1, col2 = st.columns(2)
    
    with col1:
        title2 = st.text_input("图表标题", value="计算思维重要性评价与复杂问题解决方式（Q4-Q5）")
        q4_labels2 = st.text_area("Q4选项标签（每行一个）", value="至关重要，是核心竞争力和关键能力\n比较重要，对学习有较大帮助\n重要性一般，有一定辅助作用\n不太重要\n几乎不重要，可有可无")
        q5_labels2 = st.text_area("Q5选项标签（每行一个）", value="分步拆解，逐步解决各个部分\n尝试寻找类似问题的解决经验\n直接采用常用的方法或模式\n向他人请教解决办法\n凭直觉随机尝试")
        q4_data_str = st.text_input("Q4数据（逗号分隔）", value="5.48, 15.41, 28.30, 34.52, 16.30")
        q5_data_str = st.text_input("Q5数据（逗号分隔）", value="11.70, 26.22, 26.07, 25.48, 10.52")
    
    with col2:
        color4 = st.color_picker("Q4颜色", value=COLORS_01["Q4"])
        color5 = st.color_picker("Q5颜色", value=COLORS_01["Q5"])
    
    if st.button("生成图表2"):
        try:
            q4_labels = [label.strip() for label in q4_labels2.split('\n') if label.strip()]
            q5_labels = [label.strip() for label in q5_labels2.split('\n') if label.strip()]
            q4_data = [float(x.strip()) for x in q4_data_str.split(',')]
            q5_data = [float(x.strip()) for x in q5_data_str.split(',')]
            
            draw_chart2(title2, q4_labels, q4_data, q5_labels, q5_data, color4, color5)
        except Exception as e:
            st.error(f"生成失败：{str(e)}")

# ===================== 标签页3：图表3 =====================
with tab3:
    st.header("2组横向分组条形图配置（Q6-Q7）")
    col1, col2 = st.columns(2)
    
    with col1:
        title3 = st.text_input("图表标题", value="项目式学习认知与计算思维应用场景（Q6-Q7）")
        q6_labels3 = st.text_area("Q6选项标签（每行一个）", value="以学生为中心的主动学习\n上课形式更自由\n作业量更多\n考核方式更严格\n不清楚")
        q7_labels3 = st.text_area("Q7选项标签（每行一个）", value="主要在应对考试题目时发挥\n可用于解决生活中的各类复杂问题\n作用仅适用于信息技术学科的学习和实践\n适用于科技研发和创新领域\n不太清楚能应用在哪些场景")
        q6_data_str = st.text_input("Q6数据（逗号分隔）", value="12.89, 28.44, 23.85, 24.89, 9.93")
        q7_data_str = st.text_input("Q7数据（逗号分隔）", value="6.37, 17.19, 35.41, 32.15, 8.89")
    
    with col2:
        color6 = st.color_picker("Q6颜色", value=COLORS_01["Q6"])
        color7 = st.color_picker("Q7颜色", value=COLORS_01["Q7"])
    
    if st.button("生成图表3"):
        try:
            q6_labels = [label.strip() for label in q6_labels3.split('\n') if label.strip()]
            q7_labels = [label.strip() for label in q7_labels3.split('\n') if label.strip()]
            q6_data = [float(x.strip()) for x in q6_data_str.split(',')]
            q7_data = [float(x.strip()) for x in q7_data_str.split(',')]
            
            draw_chart3(title3, q6_labels, q6_data, q7_labels, q7_data, color6, color7)
        except Exception as e:
            st.error(f"生成失败：{str(e)}")

# ===================== 标签页4：图表4 =====================
with tab4:
    st.header("双饼图配置（1行2列）")
    col1, col2 = st.columns(2)
    
    with col1:
        group_title4 = st.text_input("图表大标题", value="项目选题偏好与小组任务分配方式（题8-题9）")
        q8_short = st.text_input("左饼图标题", value="题8：项目类型偏好")
        q8_data_str = st.text_input("左饼图数据（逗号分隔）", value="24.59, 28.30, 28.59, 13.19, 5.33")
        q8_options = st.text_area("左饼图选项（每行一个）", value="贴近生活\n学科综合\n科技前沿\n教师指定\n小组创意")
        
        q9_short = st.text_input("右饼图标题", value="题9：任务分配方式")
        q9_data_str = st.text_input("右饼图数据（逗号分隔）", value="28.00, 21.33, 9.04, 17.33, 24.30")
        q9_options = st.text_area("右饼图选项（每行一个）", value="按特长分配\n轮流换角色\n听组长安排\n全员做同题\n自由选任务")
    
    with col2:
        # 颜色配置（可选）
        st.subheader("左饼图配色（可选）")
        left_colors_custom = []
        for i, c in enumerate(LEFT_COLORS):
            left_colors_custom.append(st.color_picker(f"左饼图颜色{i+1}", value=c))
        
        st.subheader("右饼图配色（可选）")
        right_colors_custom = []
        for i, c in enumerate(RIGHT_COLORS):
            right_colors_custom.append(st.color_picker(f"右饼图颜色{i+1}", value=c))
    
    if st.button("生成图表4"):
        try:
            # 数据转换
            q8_data = [float(x.strip()) for x in q8_data_str.split(',')]
            q8_options_list = [opt.strip() for opt in q8_options.split('\n') if opt.strip()]
            q9_data = [float(x.strip()) for x in q9_data_str.split(',')]
            q9_options_list = [opt.strip() for opt in q9_options.split('\n') if opt.strip()]
            
            # 构造参数
            q1_info = {
                "short_title": q8_short,
                "data": q8_data,
                "options": q8_options_list
            }
            q2_info = {
                "short_title": q9_short,
                "data": q9_data,
                "options": q9_options_list
            }
            
            draw_chart4(group_title4, q1_info, q2_info, left_colors_custom, right_colors_custom)
        except Exception as e:
            st.error(f"生成失败：{str(e)}")

# ===================== 标签页5：图表5 =====================
with tab5:
    st.header("横向堆积条形图配置（2题）")
    col1, col2 = st.columns(2)
    
    with col1:
        group_title5 = st.text_input("图表标题", value="传统课堂教学的现存不足与项目式学习改进方向（题18-题19）")
        
        q18_short = st.text_input("第一题标题", value="题18：传统教学不足")
        q18_data_str = st.text_input("第一题数据（逗号分隔）", value="25.93, 12.30, 25.93, 13.04, 22.81")
        q18_options = st.text_area("第一题选项（每行一个）", value="理论多实践少\n内容陈旧\n教师中心\n评价单一\n教法落后")
        
        q19_short = st.text_input("第二题标题", value="题19：项目改进方向")
        q19_data_str = st.text_input("第二题数据（逗号分隔）", value="22.07, 26.07, 9.63, 15.26, 26.96")
        q19_options = st.text_area("第二题选项（每行一个）", value="增实践环节\n引前沿技术\n优课堂互动\n改考核评价\n强趣味实用")
    
    with col2:
        # 配色配置
        st.subheader("堆积配色（可选）")
        colors5_custom = []
        for i, c in enumerate(COLORS_03):
            colors5_custom.append(st.color_picker(f"颜色{i+1}", value=c))
    
    if st.button("生成图表5"):
        try:
            # 数据转换
            q18_data = [float(x.strip()) for x in q18_data_str.split(',')]
            q18_options_list = [opt.strip() for opt in q18_options.split('\n') if opt.strip()]
            q19_data = [float(x.strip()) for x in q19_data_str.split(',')]
            q19_options_list = [opt.strip() for opt in q19_options.split('\n') if opt.strip()]
            
            # 构造参数
            q1_info = {
                "short_title": q18_short,
                "data": q18_data,
                "options": q18_options_list
            }
            q2_info = {
                "short_title": q19_short,
                "data": q19_data,
                "options": q19_options_list
            }
            
            draw_chart5(group_title5, q1_info, q2_info, colors5_custom)
        except Exception as e:
            st.error(f"生成失败：{str(e)}")

# ===================== 标签页6：图表6 =====================
with tab6:
    st.header("横向堆积条形图配置（3题）")
    col1, col2 = st.columns(2)
    
    with col1:
        group_title6 = st.text_input("图表标题", value="AIGC项目式学习的现存问题、任务偏好与帮助需求（题20-题22）")
        
        q20_short = st.text_input("第一题标题", value="题20：AIGC学习问题")
        q20_data_str = st.text_input("第一题数据（逗号分隔）", value="11.56, 22.22, 14.37, 26.37, 25.48")
        q20_options = st.text_area("第一题选项（每行一个）", value="影响成绩\n操作复杂\n小组矛盾\n评价不公\n能力不足")
        
        q21_short = st.text_input("第二题标题", value="题21：AIGC任务偏好")
        q21_data_str = st.text_input("第二题数据（逗号分隔）", value="10.81, 36.59, 27.85, 18.22, 6.52")
        q21_options = st.text_area("第二题选项（每行一个）", value="算法设计\n跨科解决\n创意生成\n数据可视化\n无偏好")
        
        q22_short = st.text_input("第三题标题", value="题22：AIGC帮助需求")
        q22_data_str = st.text_input("第三题数据（逗号分隔）", value="12.59, 28.00, 14.96, 22.22, 22.22")
        q22_options = st.text_area("第三题选项（每行一个）", value="指导教程\n实践资源\n技术支持\n个性建议\n成果展示")
    
    with col2:
        # 配色配置
        st.subheader("堆积配色（可选）")
        colors6_custom = []
        for i, c in enumerate(COLORS_03):
            colors6_custom.append(st.color_picker(f"颜色{i+1}", value=c))
    
    if st.button("生成图表6"):
        try:
            # 数据转换
            q20_data = [float(x.strip()) for x in q20_data_str.split(',')]
            q20_options_list = [opt.strip() for opt in q20_options.split('\n') if opt.strip()]
            q21_data = [float(x.strip()) for x in q21_data_str.split(',')]
            q21_options_list = [opt.strip() for opt in q21_options.split('\n') if opt.strip()]
            q22_data = [float(x.strip()) for x in q22_data_str.split(',')]
            q22_options_list = [opt.strip() for opt in q22_options.split('\n') if opt.strip()]
            
            # 构造参数
            q1_info = {
                "short_title": q20_short,
                "data": q20_data,
                "options": q20_options_list
            }
            q2_info = {
                "short_title": q21_short,
                "data": q21_data,
                "options": q21_options_list
            }
            q3_info = {
                "short_title": q22_short,
                "data": q22_data,
                "options": q22_options_list
            }
            
            draw_chart6(group_title6, q1_info, q2_info, q3_info, colors6_custom)
        except Exception as e:
            st.error(f"生成失败：{str(e)}")

st.markdown("---")
st.info("提示：\n1. 请将SIMHEI.TTF字体文件放在代码同目录下以确保中文正常显示\n2. 数据输入格式为逗号分隔的数字（如：10.0, 20.5, 30.0）\n3. 选项标签每行一个，数量建议不超过5个")
