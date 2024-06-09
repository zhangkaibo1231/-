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

def lbkin(x,y,z,vx,vy,vz):
	# lebai 机器人臂的数据。根据仿真环境修改这些常量。
	d = [0, 0.216363, 0, 0, 0.119808, 0.098406, 0.083254+pm.get_param('TCP')['z']]
	a = [0, 0, -0.280793, -0.259692, 0, 0]
	#alpha = [0, np.pi / 2, 0, 0, np.pi / 2, -np.pi / 2]#不可改变
	theta = np.zeros((9, 7))  # 存储8组解决方案，每组6个角度

	#注意：旋转向量的3个分量不能由欧拉角直接表示，需要修改

	# 将旋转向量转换为旋转矩阵
	v = np.array([vx, vy, vz])
	t_alpha = np.linalg.norm(v)# 旋转向量的范数
	if t_alpha ==0:
		R=np.eye(3)
	else:
		v = v / t_alpha  # 归一化旋转向量
		R = np.array([[np.cos(t_alpha), 0, np.sin(t_alpha)], [0, 1, 0], [-np.sin(t_alpha), 0, np.cos(t_alpha)]])

	# theta1
	A = R[0, 2] * d[6] - x
	B = R[1, 2] * d[6] - y
	C = d[4]
	# 第一个解，赋给一到四组
	theta[1][1] = np.arctan2(B, A) - np.arctan2(C, np.sqrt(A * A + B * B - C * C))
	theta[2][1] = theta[1][1]
	theta[3][1] = theta[1][1]
	theta[4][1] = theta[1][1]
	# 第二个解，赋给五到八组
	theta[5][1] = np.arctan2(B, A) - np.arctan2(C, -np.sqrt(A * A + B * B - C * C))
	theta[6][1] = theta[5][1]
	theta[7][1] = theta[5][1]
	theta[8][1] = theta[5][1]

	# theta5
	# 由theta[1][1]产生的第一个解，赋给一到二组
	A = np.sin(theta[1][1]) * R[0, 2] - np.cos(theta[1][1]) * R[1, 2]
	theta[1][5] = np.arctan2(np.sqrt(1 - A * A), A)
	theta[2][5] = theta[1][5]
	# 由theta[1][1]产生的第二个解，赋给三到四组
	theta[3][5] = np.arctan2(-np.sqrt(1 - A * A), A)
	theta[4][5] = theta[3][5]
	# 由theta[5][1]产生的第一个解，赋给五到六组
	A = np.sin(theta[5][1]) * R[0, 2] - np.cos(theta[5][1]) * R[1, 2]
	theta[5][5] = np.arctan2(np.sqrt(1 - A * A), A)
	theta[6][5] = theta[5][5]
	# 由theta[5][1]产生的第二个解，赋给七到八组
	theta[7][5] = np.arctan2(-np.sqrt(1 - A * A), A)
	theta[8][5] = theta[7][5]

	# theta6
	for i in range(1, 9):

		A = (-np.sin(theta[i][1]) * R[0, 1] + np.cos(theta[i][1]) * R[1, 1]) / theta[i][5]
		B = (np.sin(theta[i][1]) * R[0, 0] - np.cos(theta[i][1]) * R[1, 0]) / theta[i][5]
		theta[i][6] = np.arctan2(A, B)

	# theta2、theta3、theta4
	for i in range(1, 9, 2):

		# 先算theta2+theta3+theta4
		theta234 = np.zeros(9)
		A = R[2, 2] / np.sin(theta[i][5])
		B = (np.cos(theta[i][1]) * R[0, 2] + np.sin(theta[i][1]) * R[1, 2]) / np.sin(theta[i][5])
		theta234[i] = np.arctan2(-A, -B) - np.pi
		theta234[i + 1] = theta234[i]

		# 消去theta2+theta3，计算theta2
		A = -np.cos(theta234[i]) * np.sin(theta[i][5]) * d[6] + np.sin(theta234[i]) * d[5]
		B = -np.sin(theta234[i]) * np.sin(theta[i][5]) * d[6] - np.cos(theta234[i]) * d[5]
		C = np.cos(theta[i][1]) * x + np.sin(theta[i][1]) * y
		D = z - d[1]
		M = C - A
		N = D - B
		E = -2 * N * a[2]
		F = 2 * M * a[2]
		G = M * M + N * N + a[2] * a[2] - a[3] * a[3]
		theta[i][2] = np.arctan2(F, E) - np.arctan2(G, np.sqrt(E * E + F * F - G * G))
		theta[i + 1][2] = np.arctan2(F, E) - np.arctan2(G, -np.sqrt(E * E + F * F - G * G))

		# 用theta2反求theta2+theta3
		theta23 = np.zeros(9)
		theta23[i] = np.arctan2((N - np.sin(theta[i][2]) * a[2]) / a[3], (M - np.cos(theta[i][2]) * a[2]) / a[3])
		theta23[i + 1] = np.arctan2((N - np.sin(theta[i + 1][2]) * a[2]) / a[3], (M - np.cos(theta[i + 1][2]) * a[2]) / a[3])

		# theta3
		theta[i][3] = theta23[i] - theta[i][2]
		theta[i + 1][3] = theta23[i + 1] - theta[i + 1][2]

		# theta4
		theta[i][4] = theta234[i] - theta23[i]
		theta[i + 1][4] = theta234[i + 1] - theta23[i + 1]

	result = []
	for i in range(1, 9):
		temp = []
		for j in range(1, 7):
			temp.append(theta[i, j])
		result.append(temp)

	# 对结果进行四舍五入
	result = [np.around(matrix, decimals=6) for matrix in result]

	return result

#print(lbkin(-0.23047,0.019067,0.332325,2.322112,0.192949,-0.081607))

