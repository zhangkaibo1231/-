import pandas as pd
import numpy as np
import glob
from txt2csv.txtend import datamake
from parament import Para_Mana
pm=Para_Mana()#参数
offsets = [pm.get_param('offset_x'), pm.get_param('offset_y'), pm.get_param('offset_z')]
files = glob.glob('../txt2csv/*.txt')

data = datamake(offsets,files)
# data是一个包含所有从TXT文件提取出的数据的列表
# 将data转换为一个DataFrame
data = pd.DataFrame(data)
# 使用前一行的数据填充NaN值
data.ffill(inplace=True)
# 为DataFrame添加足够的列
while len(data.columns) < 12:
    data[len(data.columns)] = np.nan
#转换为浮点数
data = data.apply(pd.to_numeric, errors='coerce')

norm_normal = np.sqrt(data[3]**2 + data[4]**2 + data[5]**2)

# 将normal向量单位化
data[3] /= norm_normal
data[4] /= norm_normal
data[5] /= norm_normal

# 创建normal矢量
data['normal_x'] = data[3]
data['normal_y'] = data[4]
data['normal_z'] = data[5]

# 计算traj矢量
data['traj_x'] = data[0].diff().shift(-1)
data['traj_y'] = data[1].diff().shift(-1)
data['traj_z'] = data[2].diff().shift(-1)

# traj矢量的单位化处理
norm_traj = np.sqrt(data['traj_x']**2 + data['traj_y']**2 + data['traj_z']**2)
data['traj_x'] /= norm_traj
data['traj_y'] /= norm_traj
data['traj_z'] /= norm_traj

a = pm.get_param('rot')
if a == 'left':
    # 交换叉乘的顺序，先使用normal矢量叉乘traj矢量，并规范化为单位矢量
    data['cross_x'] = data['normal_y'] * data['traj_z'] - data['normal_z'] * data['traj_y']
    data['cross_y'] = data['normal_z'] * data['traj_x'] - data['normal_x'] * data['traj_z']
    data['cross_z'] = data['normal_x'] * data['traj_y'] - data['normal_y'] * data['traj_x']
else:
    # 交换叉乘的顺序，先使用traj矢量叉乘normal矢量，并规范化为单位矢量
    data['cross_x'] = data['traj_y'] * data['normal_z'] - data['traj_z'] * data['normal_y']
    data['cross_y'] = data['traj_z'] * data['normal_x'] - data['traj_x'] * data['normal_z']
    data['cross_z'] = data['traj_x'] * data['normal_y'] - data['traj_y'] * data['normal_x']

norm = np.sqrt(data['cross_x'] ** 2 + data['cross_y'] ** 2 + data['cross_z'] ** 2)
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
data.to_csv('pose.csv', index=False, header=False)