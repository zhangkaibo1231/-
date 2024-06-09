from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import numpy as np
import os
'''
# 获取当前文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 在当前目录的上一目录中的文件名
filename = 'euler.csv'
# 获取上一目录的路径
parent_dir = os.path.dirname(current_dir)
# 获取上一目录中文件的路径
file_path = os.path.join(parent_dir, filename)
# 根据文件路径读取文件
'''

# 读取csv文件，假设前三列为x, y, z坐标
df = pd.read_csv('rdp_vector.csv')
points = df[df.columns[:3]].values

hulls = []

# 每2000个点创建一个ConvexHull对象
for i in range(0, len(points), 400):
    hull = ConvexHull(points[i:i+400])
    hulls.append(hull)

# 创建一个新的图形和一个Axes3D的实例
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

# 对每一个hull进行可视化
for hull in hulls:
    # 绘制原始的点
    ax.scatter(points[:,0], points[:,1], points[:,2])

    # 为凸包添加三角形
    for s in hull.simplices:
        s = np.append(s, s[0])  # Here we cycle back to the first coordinate
        ax.plot(points[s, 0], points[s, 1], points[s, 2], 'r-')

plt.show()