import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# 读取CSV文件
data = pd.read_csv('../joint/outputmore.csv', header=None, usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, ])# 读取前九列

# 提取第2000到4000行的数据
data = data.iloc[2000:2451]

# 提取坐标
x = data[0].values
y = data[1].values
z = data[2].values

# 提取单位矢量的分量
dx = data[9].values
dy = data[10].values
dz = data[11].values

# 创建3D图形
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 绘制向量，增大箭头长度和箭头大小
ax.quiver(x, y, z, dx, dy, dz, length=1, arrow_length_ratio=0.2, normalize=True)

# 设置图形属性
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# 显示图形
plt.show()