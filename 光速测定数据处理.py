import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.table import Table

# 设置全局字体
font = FontProperties(family='SimHei', size=12)
plt.rcParams['font.family'] = font.get_name()

# 等相间距法数据处理
equidistant_data = {
    '位置': ['x0', 'x1', 'x2', 'x3', 'x4'],
    '读数(cm)': [5.00, 15.00, 25.00, 35.00, 45.00],
    'Δx = xi - x0 (cm)': [0, 10.00, 20.00, 30.00, 40.00],
    '测相信号相移距离(格)': [0, 1.4, 2.9, 4.2, 5.9],
    '测相信号相移量(弧度)': [0] + [2 * np.pi / 22 * x for x in [1.4, 2.9, 4.2, 5.9]],
    '载波波长λ = 2π / φ × 2Δx (m)': [0] + [2 * np.pi * 2 * d / (2 * np.pi / 22 * p) / 100 for d, p in zip([10, 20, 30, 40], [1.4, 2.9, 4.2, 5.9])],
    '波长平均(m)': [3.06] * 5
}
equidistant_df = pd.DataFrame(equidistant_data)
frequency = 100 * 10 ** 6
equidistant_df['光速 C = λf (m/s)'] = equidistant_df['波长平均(m)'] * frequency
accepted_speed_of_light = 2.998 * 10 ** 8
equidistant_df['误差(%)'] = np.abs((equidistant_df['光速 C = λf (m/s)'] - accepted_speed_of_light) / accepted_speed_of_light) * 100

# 等相位法数据处理
equal_phase_data = {
    '相位位置(度)': [81.82, 81.82, 81.82],
    'x0 (cm)': [4, 10, 12],
    'xi (cm)': [38.4, 45.2, 46.3],
    'x0\' (cm)': [4, 9.9, 12.1],
    'x0平均 (cm)': [4, 10, 12],
    'Di = xi - x0 (cm)': [34.4, 35.2, 34.3],
    '×2Di (cm)': [2 * 34.4, 2 * 35.2, 2 * 34.3],
    '载波波长λ = 2π / φ × 2Di (m)': [2 * np.pi * 2 * 34.4 / (81.82 * np.pi / 180) / 100,
                                       2 * np.pi * 2 * 35.2 / (81.82 * np.pi / 180) / 100,
                                       2 * np.pi * 2 * 34.3 / (81.82 * np.pi / 180) / 100],
    '波长平均λ (m)': [3.02, 3.05, 3.01]
}
equal_phase_df = pd.DataFrame(equal_phase_data)
equal_phase_df['光速 C = λf (m/s)'] = equal_phase_df['波长平均λ (m)'] * frequency
equal_phase_df['误差(%)'] = np.abs((equal_phase_df['光速 C = λf (m/s)'] - accepted_speed_of_light) / accepted_speed_of_light) * 100

# 绘制等相间距法表格图像
fig_table_equidistant, ax_table_equidistant = plt.subplots()
ax_table_equidistant.axis('off')
table_equidistant = Table(ax_table_equidistant)
nrows, ncols = equidistant_df.shape
width, height = 1.0 / ncols, 1.0 / nrows

for (i, j), val in np.ndenumerate(equidistant_df):
    cell = table_equidistant.add_cell(i, j, width, height, text=val, loc='center', edgecolor='w')
    cell.set_fontsize(14)  # 单独设置字体大小

for j, col in enumerate(equidistant_df.columns):
    cell = table_equidistant.add_cell(-1, j, width, height, text=col, loc='center', facecolor='lightgray')
    cell.set_fontsize(14)  # 单独设置字体大小

ax_table_equidistant.add_table(table_equidistant)
ax_table_equidistant.set_title('等相间距法数据表格', fontproperties=font)

# 绘制等相位法表格图像
fig_table_equal_phase, ax_table_equal_phase = plt.subplots()
ax_table_equal_phase.axis('off')
table_equal_phase = Table(ax_table_equal_phase)
nrows, ncols = equal_phase_df.shape
width, height = 1.0 / ncols, 1.0 / nrows

for (i, j), val in np.ndenumerate(equal_phase_df):
    cell = table_equal_phase.add_cell(i, j, width, height, text=val, loc='center', edgecolor='w')
    cell.set_fontsize(14)  # 单独设置字体大小

for j, col in enumerate(equal_phase_df.columns):
    cell = table_equal_phase.add_cell(-1, j, width, height, text=col, loc='center', facecolor='lightgray')
    cell.set_fontsize(14)  # 单独设置字体大小

ax_table_equal_phase.add_table(table_equal_phase)
ax_table_equal_phase.set_title('等相位法数据表格', fontproperties=font)

# 误差分析文本
equidistant_error_analysis = f"等相间距法平均误差: {equidistant_df['误差(%)'].mean():.2f}%"
equal_phase_error_analysis = f"等相位法平均误差: {equal_phase_df['误差(%)'].mean():.2f}%"

# 绘制误差柱状图
labels = ['等相间距法', '等相位法']
errors = [equidistant_df['误差(%)'].mean(), equal_phase_df['误差(%)'].mean()]

x = np.arange(len(labels))
width = 0.4

fig, ax = plt.subplots()
rects = ax.bar(x, errors, width)

ax.set_ylabel('误差(%)', fontproperties=font)
ax.set_title('不同方法光速测定误差对比', fontproperties=font)
ax.set_xticks(x)
ax.set_xticklabels(labels, fontproperties=font)


def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{:.2f}%'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontproperties=font)


autolabel(rects)

# 显示图像
plt.show()

# 打印表格
print("等相间距法数据表格：")
print(equidistant_df)
print("\n等相位法数据表格：")
print(equal_phase_df)
# 打印误差分析文本
print("\n误差分析：")
print(equidistant_error_analysis)
print(equal_phase_error_analysis)