import pandas as pd
import numpy as np

# 读取CSV文件
data = pd.read_csv('pose_rounded.csv', header=None)

# 初始化新的DataFrame用于存储结果
euler_data = pd.DataFrame()

# 将x, y, z点坐标复制到新的DataFrame
euler_data[[0, 1, 2]] = data[[0, 1, 2]]

# 计算每个位置的欧拉角
for index, row in data.iterrows():
    # 构造旋转矩阵
    ##00 01 02
    ##10 11 12
    ##20 21 22
    R = np.array([
        [row[3], row[6], row[9]],
        [row[4], row[7], row[10]],
        [row[5], row[8], row[11]]
    ])

    # 计算欧拉角
    beta = np.arctan2(-R[2,0],(R[0,0]**2+R[1,0]**2)**(1/2))
    alpha = np.arctan2(R[1,0]/np.cos(beta),R[0,0]/np.cos(beta))
    gama = np.arctan2(R[2,1]/np.cos(beta),R[2,2]/np.cos(beta))

    # 将欧拉角添加到新的DataFram2e
    euler_data.loc[index, 3] = alpha
    euler_data.loc[index, 4] = beta
    euler_data.loc[index, 5] = gama

# 对所有数据进行四舍五入，保留4位小数
euler_data = euler_data.round(4)

# 将欧拉角数据保存到CSV文件
euler_data.to_csv('euler.csv', index=False, header=False)