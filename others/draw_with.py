import matplotlib.pyplot as plt
import csv
import numpy as np

# 创建一个3D绘图对象
fig = plt.figure(figsize=(8, 6))  # 宽度和高度的尺寸，单位是英寸
ax = fig.add_subplot(111, projection='3d')

# 打开csv文件并读取位姿数据
with open('outputmore.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    vector = None
    for i, row in enumerate(reader, 1):  # 添加了enumerate函数，用于计数
        # 从csv文件的每一行中获取位姿数据
        cartesian_pose = {'x': float(row[0]), 'y': float(row[1]), 'z': float(row[2])}
        current_vector = np.array([float(row[9]), float(row[10]), float(row[11])])  # 此处索引应从0开始，因此10，11，12对应的索引为9，10，11

        # 每次读取一行就在3D图中添加一个点，并绘制一条从上一个点到这个点的线
        ax.scatter(cartesian_pose['x'], cartesian_pose['y'], cartesian_pose['z'], color='b')
        if i > 1:
            ax.plot([prev_pose['x'], cartesian_pose['x']],
                    [prev_pose['y'], cartesian_pose['y']],
                    [prev_pose['z'], cartesian_pose['z']], color='r')

        # 如果向量存在，则在图中删除
        if vector is not None:
            vector.remove()

        # 显示与当前点关联的向量
        vector = ax.quiver(cartesian_pose['x'],# - current_vector[0], #起点坐标
                           cartesian_pose['y'],# - current_vector[1],
                           cartesian_pose['z'],# - current_vector[2],
                           current_vector[0], current_vector[1], current_vector[2],
                           color='g', length=1, arrow_length_ratio=0)

        # 保存这个点的位姿，以便下一次循环可以从这个点画线到下一个点
        prev_pose = cartesian_pose

        # 更新图形并暂停一会
        plt.draw()
        plt.pause(0.01)

    # 在循环结束后保持图形显示
    plt.show()