import numpy as np
from parament import Para_Mana
pm = Para_Mana()  #参数
#   输入theta为逼近角，单位为弧度，矩阵大小1*7(第一个不采用);
#   输出J为速度雅各比矩阵，矩阵大小6*6；
#   说明：利用向量积的方法求解系统的雅各比矩阵
#   说明：此求解方法基于SDH参数建模，若MDH方法建模，需进行一定的下标改动
def jacobi(theta=np.zeros(7)):
	d = [0, 0.216363, 0, 0, 0.119808, 0.098406, 0.083254 + pm.get_param('TCP')['z']]
	a = [0, 0, -0.280793, -0.259692, 0, 0, 0]
	alpha = [0, np.pi / 2, 0, 0, np.pi / 2, -np.pi / 2, 0]  # lebai 机器人的alpha参数（以弧度为单位）
	theta[0] = 0

	# 计算关节之间的变换矩阵
	T = [np.eye(4)]
	for i in range(1, 7):
		cos_theta = np.cos(theta[i])
		sin_theta = np.sin(theta[i])
		cos_alpha = np.cos(alpha[i])
		sin_alpha = np.sin(alpha[i])
		T.append(np.array([
			[cos_theta, -sin_theta * cos_alpha, sin_theta * sin_alpha, a[i] * cos_theta],
			[sin_theta, cos_theta * cos_alpha, -cos_theta * sin_alpha, sin_theta * a[i]],
			[0, sin_alpha, cos_alpha, d[i]],
			[0, 0, 0, 1]
		]))

	# 计算相对于基坐标的变换矩阵
	trans = [np.eye(4)]
	for i in range(1, 7):
		if i == 1:
			transform = T[1]
			trans.append(transform)
		else:
			transform = np.linalg.multi_dot(T[0:i])
			trans.append(transform)

	# 提取各变换矩阵的旋转矩阵
	R = [np.eye(3)]*7
	for i in range(7):
		R[i] = trans[i][:3, :3]

	# 提取旋转矩阵第3列，即Z轴方向分量
	Z = [np.eye(3)]*7
	for i in range(7):
		Z[i] = R[i][:, 2]

	# Pi为坐标系i与世界坐标系0的相对位置
	P = [np.zeros(3)]*7
	for i in range(1,7):
		P[i] = trans[i][:3, 3]

	J = np.zeros((6, 6))
	for i in range(6):
		J[:3, i] = np.cross(Z[i], P[6] - P[i])
		J[3:, i] = Z[i]

	return J
































