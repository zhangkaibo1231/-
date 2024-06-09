import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# lebai 机器人臂的数据。根据你的仿真环境修改这些常量。
d = [0, 0.216363, 0, 0, 0.119808, 0.098406, 0.083254]
a = [0, 0, -0.280793, -0.259692, 0, 0]
alpha = [0, np.pi / 2, 0, 0, np.pi / 2, -np.pi / 2]  # lebai 机器人的alpha参数（以弧度为单位）
theta = np.zeros((9, 7))  # 存储8组解决方案，每组6个角度

def kinematics(theta_input):
    T = [np.eye(4) for _ in range(7)]  # 将变换矩阵初始化为单位矩阵

    # 计算每个关节角度的单独变换矩阵
    for i in range(1, 7):
        cos_theta = np.cos(theta_input[i])
        sin_theta = np.sin(theta_input[i])
        cos_alpha = np.cos(alpha[i - 1])
        sin_alpha = np.sin(alpha[i - 1])
        T[i] = np.array([
            [cos_theta, -sin_theta, 0, a[i - 1]],
            [sin_theta * cos_alpha, cos_theta * cos_alpha, -sin_alpha, -sin_alpha * d[i]],
            [sin_theta * sin_alpha, cos_theta * sin_alpha, cos_alpha, cos_alpha * d[i]],
            [0, 0, 0, 1]
        ])

    # 计算从基座到末端执行器的最终变换矩阵
    T06 = np.linalg.multi_dot(T[1:])  # 所有T矩阵的点积

    # 输出末端执行器的位置，用于验证
    X = T06[0, 3]
    Y = T06[1, 3]
    Z = T06[2, 3]

    return X, Y, Z


xs = []
ys = []
zs = []

# θ的随机样本
samples = np.random.uniform(low=-2*np.pi, high=2*np.pi, size=(100000, 7))

for sample in samples:
    x, y, z = kinematics(sample)
    xs.append(x)
    ys.append(y)
    zs.append(z)

fig = plt.figure(figsize=(15,5))

# 创建3D子图
ax1 = fig.add_subplot(131, projection='3d')
ax1.scatter(xs, ys, zs, s=1)
ax1.set_xlabel('X')
ax1.set_ylabel('Y')
ax1.set_zlabel('Z')
ax1.set_title('3D plot')

# 创建XY平面截面图
ax2 = fig.add_subplot(132)
ax2.scatter(xs, ys, s=1)
ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.set_title('XY plane')

# 创建XZ平面截面图
ax3 = fig.add_subplot(133)
ax3.scatter(xs, zs, s=1)
ax3.set_xlabel('X')
ax3.set_ylabel('Z')
ax3.set_title('XZ plane')

# 显示图像
plt.show()