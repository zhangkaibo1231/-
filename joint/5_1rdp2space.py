import csv
import numpy as np
from rdp import rdp

# 打开csv文件并读取数据
with open('simple_vector.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    data = [row for row in reader]

# 提取并转换点的坐标
path = np.array([[float(row[0]), float(row[1]), float(row[2])] for row in data])

# 使用RDP算法简化路径
mask = rdp(path, epsilon=0.01, return_mask=True)

# 创建一个新的空数据列表
new_data = [[''] * len(data[0]) for _ in range(len(data))]

# 仅将未被RDP算法移除的点填入新数据列表
for row, m in zip(data, mask):
    if m:
        new_data[data.index(row)] = row

# 输出新数据到CSV文件
with open('space_point.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(new_data)