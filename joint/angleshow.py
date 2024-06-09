import json
import matplotlib.pyplot as plt
import numpy as np

# 读取json文件
with open('print.json', 'r') as f:
    data = json.load(f)

# 初始化x轴和y轴的数据列表
x = []
y = [[] for _ in range(6)]  # 创建6个列表，分别对应theta[0]到theta[5]

# 初始化一个变量，用来存储累计的时间
time = 0

# 遍历数据
for item in data:
    '''
    # 对theta[0]到theta[5]的值进行处理，如果为负数，就加上2π  ##这里需要注意
    for i in range(6):
        if item['theta'][i] < 0:
            item['theta'][i] += 2 * np.pi
    '''
    # 将累计的时间添加到x轴的数据列表中
    time += item['t']
    x.append(time)

    # 将theta[0]到theta[5]的值添加到y轴的数据列表中
    for i in range(6):
        y[i].append(item['theta'][i])

# 使用plot函数绘制6条折线图，分别对应theta[0]到theta[5]
for i in range(6):
    plt.plot(x, y[i], label='theta[{}]'.format(i+1))

# 添加x轴和y轴的标签
plt.xlabel('Time(s)')
plt.ylabel('Theta (rad)')

# 添加图例
plt.legend()

# 显示图形
plt.show()