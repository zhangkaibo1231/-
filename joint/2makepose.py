import pandas as pd
import numpy as np

# 读取CSV文件，注意文件路径是 'txt2csv/output.csv'
data = pd.read_csv('../txt2csv/output.csv', header=None)

# 使用前一行的数据填充NaN值
data.ffill(inplace=True)

# 为DataFrame添加足够的列
while len(data.columns) < 12:
    data[len(data.columns)] = np.nan

# 计算normal向量的长度
norm_normal = np.sqrt(data[3]**2 + data[4]**2 + data[5]**2)

# 将normal向量单位化
data[3] /= norm_normal
data[4] /= norm_normal
data[5] /= norm_normal

# 计算traj矢量
data['traj_x'] = data[0].diff().shift(-1)
data['traj_y'] = data[1].diff().shift(-1)
data['traj_z'] = data[2].diff().shift(-1)

# traj矢量的单位化处理
norm_traj = np.sqrt(data['traj_x']**2 + data['traj_y']**2 + data['traj_z']**2)
data['traj_x'] /= norm_traj
data['traj_y'] /= norm_traj
data['traj_z'] /= norm_traj

# 填充缺失值
#data = data.fillna(0)

# 创建normal矢量
data['normal_x'] = data[3]
data['normal_y'] = data[4]
data['normal_z'] = data[5]

# 交换叉乘的顺序，先使用normal矢量叉乘traj矢量，并规范化为单位矢量
data['cross_x'] = data['normal_y'] * data['traj_z'] - data['normal_z'] * data['traj_y']
data['cross_y'] = data['normal_z'] * data['traj_x'] - data['normal_x'] * data['traj_z']
data['cross_z'] = data['normal_x'] * data['traj_y'] - data['normal_y'] * data['traj_x']

norm = np.sqrt(data['cross_x']**2 + data['cross_y']**2 + data['cross_z']**2)
data['cross_x'] /= norm
data['cross_y'] /= norm
data['cross_z'] /= norm

# 将计算结果存储到对应的列
data[6] = data['traj_x']
data[7] = data['traj_y']
data[8] = data['traj_z']
data[9] = data['cross_x']
data[10] = data['cross_y']
data[11] = data['cross_z']

# 删除计算过程中添加的列
data.drop(['traj_x', 'traj_y', 'traj_z', 'normal_x', 'normal_y', 'normal_z', 'cross_x', 'cross_y', 'cross_z'], axis=1, inplace=True)

# 将数据保存回CSV文件
data.to_csv('outputmore.csv', index=False, header=False)