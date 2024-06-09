import csv
import numpy as np
from rdp import rdp

# 打开csv文件并读取数据
with open('vector.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    data = [row for row in reader]

# 提取并转换点的坐标
path = np.array([[float(row[0]), float(row[1]), float(row[2])] for row in data])

# 使用RDP算法简化路径
mask = rdp(path, epsilon=0.0001, return_mask=True)

# 提取简化后的路径和对应的其他数据
simplified_data = [row for row, m in zip(data, mask) if m]

# 输出简化后的数据到CSV文件
with open('simple_vector.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(simplified_data)