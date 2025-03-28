import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib import rcParams

# ，根据你的情况决定是否替换SimHei
rcParams['font.sans-serif'] = ['SimHei']  
rcParams['axes.unicode_minus'] = False   


# 解析表格数据
数据1 = {
    'C_m': [4, 10, 12],
    'c_m': [38.4, 45.2, 46.3],
    'x0': [4, 9.9, 12]  # x0列最后一个值原图为空格，这里用NaN表示
}
数据1['x0'][-1] = np.nan
表格1 = pd.DataFrame(数据1)
D_i值 = [24.4, 24.3]
λ值 = [35.2, 34.3]

# 解析表格数据
数据2 = {
    '读数_X': ['X0', 'X1', 'X2', 'X3'],
    'C×V': [5.00, 15.00, 35.00, 45.00],
    '|λ1−λ2|−λ3': [10.00, 20.00, 30.00, 40.00]
}
表格2 = pd.DataFrame(数据2)
plt.figure(figsize=(14, 10))

# 第一个数据可视化
plt.subplot(2, 2, 1)
plt.plot(表格1['C_m'], 表格1['c_m'], 'o-', label='c_m 随 C_m 变化')
plt.xlabel('C_m (单位)')
plt.ylabel('c_m (单位)')
plt.title('文件1数据关系图')
plt.grid(True)

# 第二个数据可视化（柱状图）
plt.subplot(2, 2, 2)
plt.bar(表格2['读数_X'], 表格2['C×V'], alpha=0.6, label='C×V 值')
plt.xlabel('读数点')
plt.ylabel('C×V (单位)')
plt.title('文件2数据分布')
plt.legend()

# 波长计算结果可视化
plt.subplot(2, 2, 3)
plt.plot(D_i值, λ值, 's--', color='red', label='波长λ')
plt.xlabel('D_i (单位)')
plt.ylabel('λ (米)')
plt.title('波长计算结果')
plt.legend()
plt.grid(True)

# 误差分析可视化
plt.subplot(2, 2, 4)
误差值 = [2.25, 1.77]
标签 = ['误差1', '误差2']
bars = plt.bar(标签, 误差值, color=['#1f77b4', '#ff7f0e'])
plt.ylabel('误差百分比 (%)')
plt.title('实验误差分析')
# 在柱子上标注数值
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height}%', ha='center', va='bottom')

plt.tight_layout()
plt.savefig('分析结果.png', dpi=300, bbox_inches='tight')
plt.show()
