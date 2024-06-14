import json
import numpy as np
from diff_angle import dif_ang

# 读取json文件
with open('print.json', 'r') as f:
    data = json.load(f)

# 初始化一个列表来保存新的数据
new_data = []

# 初始化一个变量来保存上一组数据
last_data = None

# 遍历数据
for item in data:
    # 计算角度差
    if last_data is not None:
        theta_diff = [dif_ang(a, b) for a, b in zip(item['theta'], last_data['theta'])]
        dt = item['t']

        # 计算各关节角速度omega
        if dt != 0:  # 检查dt是否等于零
            omega = [angle_diff / dt for angle_diff in theta_diff]

            # 对所有数据进行四舍五入，保留6位小数
            omega = [round(omega_i, 6) for omega_i in omega]

            # 将omega添加到上一组数据中
            last_data['omega'] = omega

        # 将上一组数据添加到新的数据列表中
        new_data.append(last_data)

    # 更新上一组数据
    last_data = item

# 将新的数据写入json文件
with open('printmore.json', 'w') as f:
    json.dump(new_data, f)