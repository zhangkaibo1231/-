import pandas as pd
import numpy as np


def slerp(q1, q2, num_steps):
    steps = np.linspace(0, 1, num_steps)
    result = []
    for t in steps:
        dot_product = np.dot(q1, q2)
        if dot_product < 0.0:
            q2 = -q2
            dot_product = -dot_product
        if dot_product > 0.9995:
            interpolated_quat = q1 + t * (q2 - q1)
        else:
            theta_0 = np.arccos(dot_product)
            sin_theta_0 = np.sin(theta_0)
            theta = theta_0 * t
            sin_theta = np.sin(theta)
            s1 = np.cos(theta) - dot_product * sin_theta / sin_theta_0
            s2 = sin_theta / sin_theta_0
            interpolated_quat = s1 * q1 + s2 * q2
        result.append(interpolated_quat)
    return result

def read_and_interpolate(file_name, num_steps):#文件名，步长
    # 读取csv文件，设置header为None表示文件没有标题栏
    data = pd.read_csv(file_name, header=None)
    # 初始化结果数组
    result = []
    # 遍历每一行数据
    for i in range(len(data)-1):
        # 获取当前行和下一行的数据
        current_row = data.iloc[i]
        next_row = data.iloc[i+1]
        # 获取位移数据和四元数数据
        pos_current = current_row[:3].values
        quat_current = current_row[3:7].values
        pos_next = next_row[:3].values
        quat_next = next_row[3:7].values
        # 对位移数据进行插值
        pos_interpolated = np.linspace(pos_current, pos_next, num_steps)
        # 对四元数数据进行插值
        quat_interpolated = slerp(quat_current, quat_next, num_steps)
        # 将插值结果添加到结果数组
        for pos, quat in zip(pos_interpolated, quat_interpolated):
            result.append(np.concatenate((pos, quat)))
    # 将结果保存到新的csv文件，设置header和index为False表示不写入列名和行索引
    result = pd.DataFrame(result)
    result.to_csv('interpolated.csv', header=False, index=False)

# 测试
file_name = 'converted.csv'  # 替换为你的csv文件名
num_steps = 10  # 你想要的步数
read_and_interpolate(file_name, num_steps)