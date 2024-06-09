#vector.csv为路径点，space_point.csv为过度简化路径，仅为碰撞检测时构造打印体
import csv
import json
import time
import numpy as np
from URIK2 import lbkin
from model_space import model_space
from diff_angle import dif_ang

import os
import sys
# 获取当前脚本的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取parament.py所在的目录
parent_dir = os.path.dirname(current_dir)
# 将parament.py所在的目录添加到sys.path
sys.path.append(parent_dir)
# 导入parament.py
from parament import Para_Mana
pm=Para_Mana()#参数



# 设置欧氏空间速度参数m/s,默认0.01
v = pm.get_param('v')

start = time.time()

# 读取打印点CSV
with open('simple_vector.csv', 'r') as f:
    reader = csv.reader(f)
    data = list(reader)

data_len=len(data)

# 读取space_point.csv
with open('space_point.csv', 'r') as f:
    reader = csv.reader(f)
    space_data = list(reader)

# 初始化结果,上一个点,上一个角度
result = []
last_point = None
last_theta = None

# 遍历数据
theta_weights = np.array([1.25, 1.15, 1.05, 1.5, 1.5, 0.75])  # 各关节加权比重theta1-theta6

for k in range(len(data)):
    # 获取x, y, z, vx, vy, vz
    x, y, z, vx, vy, vz = data[k][:6]
    x, y, z, vx, vy, vz = float(x), float(y), float(z), float(vx), float(vy), float(vz)
    current_point = np.array([x, y, z])

    # 计算运动时间(上一点到当前点),最小间隔要大于0.01秒
    if last_point is None:
        t = 0
    else:
        t = np.linalg.norm(current_point - last_point) / v
        t=t.round(2)#保留2位小数
    last_point = current_point

    # 调用lbkin函数
    thetas = lbkin(x, y, z, vx, vy, vz)
    # 过滤nan值
    thetas = [theta for theta in thetas if not any(np.isnan(val) for val in theta)]
    # 初始化theta列表
    theta_list = []
    sort_values = []

    # 定义上一组解
    if last_theta is None:
        last_theta = np.zeros(6).tolist()

    ##对每一组末端位姿对应的各组关节转角进行筛选
    for theta in thetas:
        ##将符合碰撞检测条件的关节转角组添加到theta_list中
        # 初始化计数器
        count = 0
        # 遍历点,进行碰撞检测
        if k == 0:
            theta_list.append(list(theta))
        for j in range(0, k):#起始行到当前行
            # 获取点坐标
            point = space_data[j][:3]
            # 如果不是空白行，将其转换为浮点数
            if any(point):
                point = np.array(point).astype(float)
            else:
                break
            # 调用model_space函数
            if model_space(theta, point) == 'no':
                count += 1
        # 如果没有超过10个True，将该解添加到theta_list中
        if count > 10:
            continue
        else:
            theta_list.append(list(theta))

    # 对符合条件的关节转角组进行进一步筛选，使用dif_ang()函数计算与上一组结果的角度差,与权重系数计算得到权重值
    for theta in theta_list:
        theta_diff = [dif_ang(a, b) for a, b in
                      zip(theta, last_theta)]
        sort_value = np.dot(np.abs(np.array(theta_diff)), theta_weights) - 0.5 * np.abs(np.cos(theta[4]))  # 计算加权比重
        sort_values.append(sort_value)

    # 如果theta列表为空，打印提示信息
    if not theta_list:
        print(f"###数据点{k+1}无结果，已跳过###")
    # 如果theta列表不为空，将该解保存到结果中
    if theta_list:
        min_index = np.argmin(sort_values)
        last_theta = theta_list[min_index]
        result.append({'x': x, 'y': y, 'z': z, 'vx': vx, 'vy': vy, 'vz': vz, 'theta': last_theta, 't': t})
    print(f"当前已执行到第{k+1}/{data_len}行")  # 打印当前执行到的行数

# 将结果保存到json文件
with open('print.json', 'w') as f:
    json.dump(result, f)
end=time.time()
print(f"计算时长：{end - start} 秒")