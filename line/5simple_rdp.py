import csv
import numpy as np
from rdp import rdp
# 导入parament.py
from parament import Para_Mana
pm=Para_Mana()#参数


# 打开csv文件并读取数据
with open('euler.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    data = [row for row in reader]

# 提取并转换点的坐标
path = np.array([[float(row[0]), float(row[1]), float(row[2])] for row in data])

# 使用RDP算法简化路径
mask = rdp(path, epsilon=pm.get_param('epsilon'), return_mask=True)

# 提取简化后的路径和对应的其他数据
simplified_data = [row for row, m in zip(data, mask) if m]

# 输出简化后的数据到CSV文件
with open('simple_euler.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(simplified_data)