import json
import matplotlib.pyplot as plt
import numpy as np

# 读取json文件
with open('printmore.json', 'r') as f:
    data = json.load(f)

# 初始化x轴和y轴的数据列表
x = []
y = [[] for _ in range(6)]  # 创建6个列表，分别对应omega[0]到omega[5]

# 初始化一个变量，用来存储累计的时间
time = 0

# 遍历数据
for item in data:

    # 将累计的时间添加到x轴的数据列表中
    time += item['t']
    x.append(time)

    # 检查 'omega' 键是否存在
    if 'omega' in item:
        # 将omega[0]到omega[5]的值添加到y轴的数据列表中
        for i in range(6):
            y[i].append(item['omega'][i])
    else:
        # 如果 'omega' 键不存在，给它一个默认值（例如，全零）
        for i in range(6):
            y[i].append(0)

# 使用plot函数绘制6条折线图，分别对应theta[0]到theta[5]
for i in range(6):
    plt.plot(x, y[i], label='omega[{}]'.format(i+1))

# 添加x轴和y轴的标签
plt.xlabel('Time(s)')
plt.ylabel('omega (rad/s)')

# 添加图例
plt.legend()

# 显示图形
plt.show()