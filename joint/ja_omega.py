import json
import numpy as np
from jacobi import jacobi  # 导入jacobi函数

# 读取json文件
with open('print.json', 'r') as f:
    data = json.load(f)

# 初始化一个列表来保存新的数据
new_data = []

# 初始化一个变量来保存上一组数据
last_data = None

# 遍历数据
for item in data:
    # 计算位姿之差
    if last_data is not None:
        dx = item['x'] - last_data['x']
        dy = item['y'] - last_data['y']
        dz = item['z'] - last_data['z']
        dvx = item['vx'] - last_data['vx']
        dvy = item['vy'] - last_data['vy']
        dvz = item['vz'] - last_data['vz']

        # 计算雅各比矩阵
        theta = [0] + item['theta']
        J = jacobi(np.array(theta))

        # 计算位姿分量速度
        dt = item['t']
        if dt != 0:  # 检查dt是否等于零
            v = np.array([dx, dy, dz, dvx, dvy, dvz]) / dt

            # 计算各关节角速度omega
            omega = np.linalg.pinv(J).dot(v)  # 使用雅各比矩阵的逆

            # 对所有数据进行四舍五入，保留6位小数
            omega = omega.round(6)

            # 将omega添加到上一组数据中
            last_data['omega'] = omega.tolist()

        # 将上一组数据添加到新的数据列表中
        new_data.append(last_data)

        # 更新上一组数据
    last_data = item

    # 更新上一组数据
    last_data = item

# 将新的数据写入json文件
with open('printmore.json', 'w') as f:
    json.dump(new_data, f)