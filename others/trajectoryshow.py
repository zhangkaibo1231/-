import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# 读取CSV文件
data = pd.read_csv('../joint/outputmore.csv', header=None, usecols=[0, 1, 2])  # 只读取前三列

# 提取第2000到4000行的数据
data = data.iloc[2000:2451]

# 提取坐标
x = data[0].values
y = data[1].values
z = data[2].values

# 计算位移向量
dx = np.diff(x)
dy = np.diff(y)
dz = np.diff(z)

# 添加一个0到最后一个位移，使得位移向量的数量与点的数量相同
dx = np.append(dx, 0)
dy = np.append(dy, 0)
dz = np.append(dz, 0)

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