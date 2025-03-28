import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 设置 matplotlib 的字体，你可以根据自己的系统选择合适的字体
plt.rcParams['font.family'] = 'SimHei'  
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

#这是我的原始数据，根据实际情况输入你的
data = {
    "次数": [200, 400, 600, 800, 1000, 1200],
    "平面镜位置": [53.63201, 53.7037, 53.76111, 53.82245, 53.89835, 53.97285]
}
df = pd.DataFrame(data)

# 逐差法
group1 = df["平面镜位置"][:3].values  # 前三组
group2 = df["平面镜位置"][3:].values  # 后三组
delta_d = group2 - group1
delta_N = 600  # 每次的ΔN为600次
delta_d_avg = np.mean(delta_d)

# 计算波长 nm
lambda_wave = 2 * delta_d_avg * 1e6 / delta_N  # 1 mm = 1e6 nm

# 数据可视化
plt.figure(figsize=(10, 5))
plt.plot(df["次数"], df["平面镜位置"], "bo-", label="原始数据")
plt.xlabel("次数")
plt.ylabel("平面镜位置 (mm)")
plt.title("平面镜位置随干涉次数变化")
plt.grid(True)
plt.legend()

# 绘制表格
fig, ax = plt.subplots(figsize=(6, 2))
ax.axis("off")
table_data = [
    ["Δd1 (mm)", delta_d[0]],
    ["Δd2 (mm)", delta_d[1]],
    ["Δd3 (mm)", delta_d[2]],
    ["平均Δd (mm)", delta_d_avg],
    ["计算波长 (nm)", f"{lambda_wave:.2f}"]
]
table = ax.table(cellText=table_data, loc="center", cellLoc="left")
table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(1, 1.5)

plt.show()

print(f"逐差法计算波长：{lambda_wave:.2f} nm")

# 误差分析
lambda_theory = 650  # 理论波长（nm）
abs_error = abs(lambda_wave - lambda_theory)
rel_error = (abs_error / lambda_theory) * 100

# 假设 sigma_lambda 是 delta_d 波动导致的波长波动
sigma_lambda = np.std(2 * delta_d * 1e6 / delta_N)

# 误差来源可视化
error_sources = {
    "测量误差 (±0.001 mm)": 0.001 * 2e6 / 600,
    "Δd波动": sigma_lambda,
    "系统误差（理论值标定）": 5  # 假设标定误差为5 nm
}
labels = list(error_sources.keys())
values = list(error_sources.values())

plt.figure(figsize=(8, 4))
bars = plt.barh(labels, values, color=["#ff9999", "#66b3ff", "#99ff99"])
plt.xlabel("波长误差贡献 (nm)")
plt.title("主要误差来源贡献分析")
plt.grid(axis="x", linestyle="--")

for bar in bars:
    width = bar.get_width()
    plt.text(width, bar.get_y() + bar.get_height()/2, f'{width:.2f}', ha='left', va='center')

plt.show()

# 输出误差
print(f"绝对误差：{abs_error:.2f} nm")
print(f"相对误差：{rel_error:.2f}%")
print(f"Δd波动导致的波长波动：±{sigma_lambda:.2f} nm")
    
