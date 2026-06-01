import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from collections import Counter
import networkx as nx
import warnings
import os
import tempfile
import zipfile
from matplotlib.font_manager import FontProperties

# 忽略警告
warnings.filterwarnings('ignore')

# ===================== 【核心】Streamlit Cloud 中文字体配置 =====================
FONT_PATH = "./SIMHEI.TTF"
my_font = FontProperties(fname=FONT_PATH)
# 全局设置字体（兼容 networkx + matplotlib）
plt.rcParams['font.family'] = my_font.get_name()
plt.rcParams["axes.unicode_minus"] = False
# ============================================================================

class LagSequentialAnalysis:
    def __init__(self, data, behavior_mapping, unique_behaviors, output_dir):
        self.data = data
        self.output_dir = output_dir
        self.behavior_mapping = behavior_mapping
        self.unique_behaviors = unique_behaviors
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        self.students = self.data.iloc[:, 0].values
        self.sequences = self.data.iloc[:, 1:].values
        self.all_behaviors = []
        self.behavior_list = []
        
        for idx, row in enumerate(self.sequences):
            student_behaviors = []
            for b in row:
                if pd.notna(b) and str(b).strip() not in ['', 'nan']:
                    behavior_code = str(b).strip()
                    behavior_cn = self.behavior_mapping.get(behavior_code, behavior_code)
                    student_behaviors.append(behavior_cn)
            self.behavior_list.append(student_behaviors)
            self.all_behaviors.extend(student_behaviors)
        
        self.log_content = []
        
    def log(self, text):
        self.log_content.append(text)
    
    def save_log(self):
        log_path = os.path.join(self.output_dir, '分析日志.txt')
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.log_content))
    
    # 1. 行为频次统计
    def behavior_frequency(self):
        freq = Counter(self.all_behaviors)
        freq_df = pd.DataFrame.from_dict(freq, orient='index', columns=['频次'])
        freq_df['百分比'] = (freq_df['频次'] / freq_df['频次'].sum() * 100).round(2)
        freq_df = freq_df.reindex(self.unique_behaviors, fill_value=0)
        freq_path = os.path.join(self.output_dir, '01_行为频次统计.csv')
        freq_df.to_csv(freq_path, encoding='utf-8-sig')
        return freq_df
    
    # 2. 转换矩阵
    def transition_frequency_matrix(self):
        transition_matrix = pd.DataFrame(0, index=self.unique_behaviors, columns=self.unique_behaviors)
        for behaviors in self.behavior_list:
            for i in range(len(behaviors)-1):
                f, t = behaviors[i], behaviors[i+1]
                if f in self.unique_behaviors and t in self.unique_behaviors:
                    transition_matrix.loc[f, t] += 1
        
        row_sums = transition_matrix.sum(axis=1)
        transition_prob = transition_matrix.div(row_sums, axis=0).fillna(0)
        
        transition_matrix.to_csv(os.path.join(self.output_dir, '02_转换频率矩阵.csv'), encoding='utf-8-sig')
        transition_prob.to_csv(os.path.join(self.output_dir, '02_转换概率矩阵.csv'), encoding='utf-8-sig')
        return transition_matrix, transition_prob
    
    # 3. 调整残差
    def adjusted_residuals(self, transition_matrix):
        row_totals = transition_matrix.sum(axis=1)
        col_totals = transition_matrix.sum(axis=0)
        total = transition_matrix.sum().sum()
        expected = pd.DataFrame(0.0, index=self.unique_behaviors, columns=self.unique_behaviors)
        
        for i in self.unique_behaviors:
            for j in self.unique_behaviors:
                expected.loc[i,j] = (row_totals[i]*col_totals[j])/total if total>0 else 0
        
        adj_res = pd.DataFrame(0.0, index=self.unique_behaviors, columns=self.unique_behaviors)
        for i in self.unique_behaviors:
            for j in self.unique_behaviors:
                obs, exp = transition_matrix.loc[i,j], expected.loc[i,j]
                if exp>0:
                    res = (obs-exp)/np.sqrt(exp)
                    rp, cp = row_totals[i]/total if total>0 else 0, col_totals[j]/total if total>0 else 0
                    adj_f = np.sqrt((1-rp)*(1-cp)) if np.sqrt((1-rp)*(1-cp))>0 else 1
                    adj_res.loc[i,j] = res/adj_f
        
        z_details = []
        for i in self.unique_behaviors:
            for j in self.unique_behaviors:
                val = adj_res.loc[i,j]
                abs_v = abs(val)
                sig = "***" if abs_v>3.29 else "**" if abs_v>2.58 else "*" if abs_v>1.96 else ""
                dir = "增强" if val>0 else "减弱" if val<0 else "无"
                z_details.append({"起始":i,"目标":j,"Z值":round(val,3),"显著性":sig,"方向":dir})
        
        z_df = pd.DataFrame(z_details).sort_values("Z值",ascending=False)
        adj_res.to_csv(os.path.join(self.output_dir, '03_调整残差矩阵.csv'), encoding='utf-8-sig')
        z_df.to_csv(os.path.join(self.output_dir, '03_全部Z值详情.csv'), index=False, encoding='utf-8-sig')
        return adj_res, z_df
    
    # 4. 个体模式
    def individual_patterns(self):
        ind_data = []
        for s, b_list in zip(self.students, self.behavior_list):
            trans = []
            mat = pd.DataFrame(0,index=self.unique_behaviors,columns=self.unique_behaviors)
            for i in range(len(b_list)-1):
                f,t = b_list[i],b_list[i+1]
                if f in self.unique_behaviors and t in self.unique_behaviors:
                    mat.loc[f,t] +=1
                    trans.append(f"{f}→{t}")
            ind_data.append({
                "学生":s,"序列":"→".join(b_list),"转换":"、".join(trans),
                "长度":len(b_list),"转换次数":len(trans)
            })
        df = pd.DataFrame(ind_data)
        df.to_csv(os.path.join(self.output_dir, '04_个体转换模式.csv'), index=False, encoding='utf-8-sig')
        return df
    
    # 5. 序列指标
    def sequence_metrics(self):
        metrics = []
        for s, b_list in zip(self.students, self.behavior_list):
            l = len(b_list)
            u = len(set(b_list))
            div = u/l if l>0 else 0
            trans = [f"{b_list[i]}→{b_list[i+1]}" for i in range(len(b_list)-1)]
            ent = -sum([c/len(trans)*np.log2(c/len(trans)) for c in Counter(trans).values()]) if trans else 0
            metrics.append({"学生":s,"长度":l,"行为数":u,"多样性":round(div,3),"熵":round(ent,3)})
        df = pd.DataFrame(metrics)
        df.to_csv(os.path.join(self.output_dir, '05_序列指标.csv'), index=False, encoding='utf-8-sig')
        return df
    
    # 6. 转换网络图（✅ 修复所有参数错误 + 字体兼容）
    def plot_transition_graph(self, trans_mat, adj_res):
        fig, ax = plt.subplots(figsize=(12,10))
        G = nx.DiGraph()
        for b in self.unique_behaviors: 
            G.add_node(b)
        
        # 添加显著边
        for i,f in enumerate(self.unique_behaviors):
            for j,t in enumerate(self.unique_behaviors):
                z = adj_res.iloc[i,j]
                if abs(z) > 1.96:
                    G.add_edge(f,t, weight=trans_mat.iloc[i,j], z_score=z)
        
        pos = nx.spring_layout(G, seed=42, k=3)
        nx.draw_networkx_nodes(G, pos, node_size=4000, node_color='#F4F6F9', 
                              edgecolors='#333', linewidths=3, ax=ax)
        
        if len(G.edges()) > 0:
            weights = [G[u][v]['weight'] for u,v in G.edges()]
            colors = ['#D62728' if G[u][v]['z_score']>1.96 else '#1F77B4' for u,v in G.edges()]
            max_w = max(weights) if max(weights) > 0 else 1
            widths = [w/max_w*8+3 for w in weights]
            
            nx.draw_networkx_edges(G,pos,width=widths,edge_color=colors,arrowsize=35,
                                  connectionstyle='arc3,rad=0.15',node_size=4000,alpha=0.85,ax=ax)
            
            # 边标签（✅ 移除错误参数 fontproperties）
            labels = {(u,v):f"{u}→{v}\nZ={G[u][v]['z_score']:.2f}" for u,v in G.edges()}
            nx.draw_networkx_edge_labels(
                G, pos, edge_labels=labels, 
                font_size=18, font_weight='bold',
                label_pos=0.25, ax=ax
            )
        
        # 节点标签（✅ 移除错误参数 fontproperties）
        nx.draw_networkx_labels(
            G, pos, 
            font_size=24, font_weight='bold',
            ax=ax
        )
        
        ax.axis('off')
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, '06_行为转换图.png'), 
                    dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
    
    # 7. 热图（✅ 字体兼容）
    def plot_heatmaps(self, trans_mat, adj_res):
        fig, axes = plt.subplots(2,2,figsize=(16,14))
        
        # 频率热图
        sns.heatmap(trans_mat, annot=True, fmt='g', cmap='Blues', ax=axes[0,0],
                    annot_kws={'size':20,'weight':'bold'})
        axes[0,0].set_title('转换频率',fontsize=22)
        axes[0,0].tick_params(labelsize=16)
        
        # 残差热图
        vmax = max(abs(adj_res.min().min()), adj_res.max().max())
        sns.heatmap(adj_res, annot=True, fmt='.2f', cmap='RdBu_r', center=0, ax=axes[0,1],
                    annot_kws={'size':20,'weight':'bold'})
        axes[0,1].set_title('调整残差(Z值)',fontsize=22)
        axes[0,1].tick_params(labelsize=16)
        
        # 显著性热图
        sig = np.where(abs(adj_res)>3.29,3,np.where(abs(adj_res)>2.58,2,np.where(abs(adj_res)>1.96,1,0)))
        sns.heatmap(sig, annot=True, fmt='g', cmap='YlOrRd', ax=axes[1,0],
                    annot_kws={'size':20,'weight':'bold'})
        axes[1,0].set_title('显著性(0-无,3-极高)',fontsize=22)
        axes[1,0].tick_params(labelsize=16)
        
        # 正向显著
        pos_sig = adj_res.copy()
        pos_sig[pos_sig<1.96] = 0
        sns.heatmap(pos_sig, annot=True, fmt='.2f', cmap='Greens', ax=axes[1,1],
                    annot_kws={'size':20,'weight':'bold'})
        axes[1,1].set_title('增强转换(Z>1.96)',fontsize=22)
        axes[1,1].tick_params(labelsize=16)
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, '07_转换热图.png'), 
                    dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
    
    # 8. 汇总Excel
    def save_excel(self, freq_df, trans_mat, adj_res, z_df, metrics_df):
        path = os.path.join(self.output_dir, '00_完整分析结果.xlsx')
        with pd.ExcelWriter(path, engine='openpyxl') as w:
            freq_df.to_excel(w, sheet_name='频次统计')
            trans_mat.to_excel(w, sheet_name='转换矩阵')
            adj_res.to_excel(w, sheet_name='调整残差')
            z_df.to_excel(w, sheet_name='Z值详情', index=False)
            metrics_df.to_excel(w, sheet_name='序列指标', index=False)
    
    # 运行全分析
    def run(self):
        freq = self.behavior_frequency()
        trans_mat, trans_prob = self.transition_frequency_matrix()
        adj_res, z_df = self.adjusted_residuals(trans_mat)
        self.individual_patterns()
        metrics = self.sequence_metrics()
        self.plot_transition_graph(trans_mat, adj_res)
        self.plot_heatmaps(trans_mat, adj_res)
        self.save_excel(freq, trans_mat, adj_res, z_df, metrics)
        self.save_log()
        return self.output_dir

# ===================== Streamlit 主程序 =====================
def main():
    st.set_page_config(page_title="滞后序列分析工具", layout="wide")
    st.title("📊 滞后序列分析 LSA - 交互式工具")
    st.markdown("---")

    # 行为配置
    st.sidebar.header("⚙️ 行为配置")
    behavior_num = st.sidebar.selectbox("行为数量", options=[2,3,4,5,6,7,8], index=2)
    
    st.subheader("📝 设置行为映射（英文编码 → 中文名称）")
    behavior_mapping = {}
    unique_behaviors = []
    
    cols = st.columns(2)
    for i in range(behavior_num):
        with cols[0]:
            en = st.text_input(f"行为{i+1} 英文编码", value=f"CODE{i+1}", key=f"en_{i}")
        with cols[1]:
            cn = st.text_input(f"行为{i+1} 中文名称", value=f"行为{i+1}", key=f"cn_{i}")
        behavior_mapping[en] = cn
        unique_behaviors.append(cn)
    
    st.markdown("---")
    
    # 文件上传
    st.subheader("📁 上传行为序列CSV文件")
    uploaded_file = st.file_uploader("上传CSV（第一列：学生编号，其余列：行为序列）", type=["csv"])
    
    if uploaded_file is not None and st.button("🚀 运行滞后序列分析", type="primary"):
        with st.spinner("正在分析中... 请稍候"):
            # 读取数据
            try:
                df = pd.read_csv(uploaded_file, sep=None, engine="python", header=None, encoding="utf-8")
            except:
                df = pd.read_csv(uploaded_file, header=None, encoding="utf-8")
            
            temp_dir = tempfile.mkdtemp()
            lsa = LagSequentialAnalysis(df, behavior_mapping, unique_behaviors, temp_dir)
            output_dir = lsa.run()
            
            # 打包ZIP
            zip_path = os.path.join(temp_dir, "滞后序列分析结果.zip")
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
                for root, dirs, files in os.walk(output_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zf.write(file_path, file)
            
            # 下载
            with open(zip_path, "rb") as f:
                st.download_button(
                    label="📥 下载全部分析结果（ZIP）",
                    data=f,
                    file_name="滞后序列分析结果.zip",
                    mime="application/zip"
                )
            
            st.success("✅ 分析完成！点击上方按钮下载结果")

if __name__ == "__main__":
    main()
