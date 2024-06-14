import pandas as pd
import numpy as np
import cv2

# 读取CSV文件
data = pd.read_csv('pose.csv', header=None)

# 计算每个位置的旋转向量分量
for index, row in data.iterrows():
    # 构造旋转矩阵
    R = np.array([
        [row[3], row[6], row[9]],
        [row[4], row[7], row[10]],
        [row[5], row[8], row[11]]
    ])
    # 使用cv2.Rodrigues()将旋转矩阵转换为旋转向量
    rotation_vector, _ = cv2.Rodrigues(R)

    # 将旋转向量分量添加到原始DataFrame
    data.loc[index, 'vx'] = rotation_vector[0]
    data.loc[index, 'vy'] = rotation_vector[1]
    data.loc[index, 'vz'] = rotation_vector[2]

# 将前三列单位由毫米改为米
data[[0, 1, 2]] = data[[0, 1, 2]] / 1000

# 将前三列和旋转向量分量复制到新的DataFrame
vec_data = data[[0, 1, 2, 'vx', 'vy', 'vz']]

# 对所有数据进行四舍五入，保留6位小数
vec_data = vec_data.round(6)

# 将旋转向量数据保存到CSV文件
vec_data.to_csv('vector.csv', index=False, header=False)