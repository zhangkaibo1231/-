import numpy as np

import sys
import os
# 获取当前脚本的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取parament.py所在的目录
parent_dir = os.path.dirname(current_dir)
# 将parament.py所在的目录添加到sys.path
sys.path.append(parent_dir)
# 导入parament.py
from parament import Para_Mana
pm = Para_Mana()  #参数

def lbkin(x, y, z, vx, vy, vz):
    #lebai 机器人臂的数据。根据仿真环境修改这些常量。
    d = [0, 0.216363, 0, 0, 0.119808, 0.098406, 0.083254 + pm.get_param('TCP')['z']]
    a = [0, 0, -0.280793, -0.259692, 0, 0, 0]
    #alpha = [0, np.pi / 2, 0, 0, np.pi / 2, -np.pi / 2, 0]#不能改变
    theta = np.zeros((9, 7))  # 存储8组解决方案，每组6个角度

    # 将旋转向量转换为旋转矩阵
    v = np.array([vx, vy, vz])
    t_alpha = np.linalg.norm(v)  # 旋转向量的范数
    if t_alpha == 0:
        R = np.eye(3)
    else:
        v = v / t_alpha  # 归一化旋转向量
        R = np.array([[np.cos(t_alpha), 0, np.sin(t_alpha)], [0, 1, 0], [-np.sin(t_alpha), 0, np.cos(t_alpha)]])

    # theta1
    A1 = x - R[0, 2] * d[6]
    B1 = y - R[1, 2] * d[6]
    # theta1第一个解
    theta[1][1] = np.arctan2(d[4], np.sqrt(A1 * A1 + B1 * B1 - d[4] * d[4])) + np.arctan2(B1, A1)
    theta[2][1] = theta[1][1]
    theta[3][1] = theta[1][1]
    theta[4][1] = theta[1][1]
    # theta6
    A6 = R[1, 0] * np.cos(theta[1][1]) - R[0, 0] * np.sin(theta[1][1])
    B6 = R[1, 1] * np.cos(theta[1][1]) - R[0, 1] * np.sin(theta[1][1])
    theta[1][6] = np.arctan2(0, 1) - np.arctan2(B6, A6)  # theta6第一个解
    theta[2][6] = theta[1][6]
    theta[3][6] = np.arctan2(0, -1) - np.arctan2(B6, A6)  # theta6第二个解
    theta[4][6] = theta[3][6]
    # theta1第二个解
    theta[5][1] = np.arctan2(d[4], -np.sqrt(A1 * A1 + B1 * B1 - d[4] * d[4])) + np.arctan2(B1, A1)
    theta[6][1] = theta[5][1]
    theta[7][1] = theta[5][1]
    theta[8][1] = theta[5][1]
    #theta6
    A6 = R[1, 0] * np.cos(theta[5][1]) - R[0, 0] * np.sin(theta[5][1])
    B6 = R[1, 1] * np.cos(theta[5][1]) - R[0, 1] * np.sin(theta[5][1])
    theta[5][6] = np.arctan2(0, 1) - np.arctan2(B6, A6)  # theta6第三个解
    theta[6][6] = theta[5][6]
    theta[7][6] = np.arctan2(0, -1) - np.arctan2(B6, A6)  # theta6第四个解
    theta[8][6] = theta[7][6]

    for i in range(1, 9):  #[1,2,3,4,5,6,7,8]
        q1=theta[i][1]
        q6=theta[i][6]
        #求theta3、theta(2+3)及theta2
        k = -1 ** i  #得到theta3在同一组theta1与theta6的变量
        P = np.cos(q1) * (x - R[0, 2] * d[6] + d[5] * R[0, 1] * np.cos(q6) + d[5] * R[0, 0] * np.sin(q6)) + np.sin(q1) * (y - R[1, 2] * d[6] + d[5] * R[1, 1] * np.cos(q6) + d[5] * R[1, 0] * np.sin(q6))
        Q = z - d[1] - R[2, 2] * d[6] + d[5] * R[2, 1] * np.cos(q6) + d[5] * R[2, 0] * np.sin(q6)
        M = (P * P + Q * Q - a[2] * a[2] - a[3] * a[3]) / (2 * a[2] * a[3])
        N = k * np.sqrt(1 - M * M)
        A23 = 2 * a[3] * P
        B23 = 2 * a[3] * Q
        C23 = a[3] * a[3] + P * P + Q * Q - a[2] * a[2]
        theta[i][3] = np.arctan2(N, M)
        q23 = np.arctan2(k * np.sqrt(A23 * A23 + B23 * B23 - C23 * C23), C23) + np.arctan2(B23, A23)
        theta[i][2] = q23 - theta[i][3]

        #theta5
        A5 = (-R[1, 0] * np.cos(q1) * np.cos(q6) + R[0, 0] * np.cos(q6) * np.sin(q1) + R[1, 1] * np.cos(q1) * np.sin(q6) - R[0, 1] * np.sin(q1) * np.sin(q6))
        B5 = R[0, 2] * np.sin(q1) - R[1, 2] * np.cos(q1)
        theta[i][5] = np.arctan2(0, 1) + np.arctan2(A5, B5)

        #通过求theta(2+3+4)求theta4
        A4 = R[2, 0] * np.cos(theta[i][5]) * np.cos(q6) - R[2, 2] * np.sin(theta[i][5]) - R[2, 1] * np.cos(theta[i][5]) * np.sin(q6)
        B4 = -np.cos(q1) * (R[0, 2] * np.sin(theta[i][5]) - R[0, 0] * np.cos(theta[i][5]) * np.cos(q6) + R[0, 1] * np.cos(theta[i][5]) * np.sin(q6)) - np.sin(q1) * (
                    R[1, 2] * np.sin(theta[i][5]) - R[1, 0] * np.cos(theta[i][5]) * np.cos(q6) + R[1, 1] * np.cos(theta[i][5]) * np.sin(q6))
        q234 = np.arctan2(A4, B4)
        theta[i][4] = q234 - q23

    result = []
    for i in range(1, 9):
        temp = []
        for j in range(1, 7):
            temp.append(theta[i, j])
        result.append(temp)

    # 对结果进行四舍五入
    #result = [np.around(matrix, decimals=6) for matrix in result]

    return result

print(lbkin(-0.234786,0.017397,0.308701,2.823883,0.803637,-0.126561))