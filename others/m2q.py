import pandas as pd
import numpy as np
from scipy.spatial.transform import Rotation as R

def convert_rotation_to_quaternion(file_name):
    # 读取csv文件，没有标题栏
    data = pd.read_csv(file_name, header=None)
    # 初始化结果列表
    result = []
    # 遍历数据的每一行
    for index, row in data.iterrows():
        # 提取点的坐标和旋转矩阵
        pos = row[:3].values
        rot_matrix = np.array([row[3:6].values, row[6:9].values, row[9:12].values])
        # 将旋转矩阵转换为四元数
        r = R.from_matrix(rot_matrix)
        quat = r.as_quat()
        # 将结果添加到结果列表
        result.append(np.concatenate((pos, quat)))
    # 将结果保存到新的csv文件
    result = pd.DataFrame(result)
    result = result.round(6)#保留六位小数
    result.to_csv('converted.csv', header=False, index=False)

# 测试
file_name = '../joint/outputmore.csv'  # 替换为你的csv文件名
convert_rotation_to_quaternion(file_name)

