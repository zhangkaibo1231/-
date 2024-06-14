import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def fkr(ang):
    d = [0, 0.216363, 0, 0, 0.119808, 0.098406, 0.083254 ]
    a = [0, 0, -0.280793, -0.259692, 0, 0, 0]
    alpha = [0,  np.pi / 2, 0, 0, np.pi / 2, -np.pi / 2, 0]  # lebai 机器人的alpha参数（以弧度为单位）
    #theta = np.zeros(7)  # 每个关节的角度位置
    #theta[1], theta[2], theta[3], theta[4], theta[5], theta[6] = [float(val) for val in input("请输入各关节角度 1, 2, 3, 4, 5, 6:\n").split()]
    ang = np.array(ang)  # 把输入参数转换为numpy数组
    theta = np.insert(ang, 0, 0)  # 在index为0的位置插入0

    # 计算关节之间的变换矩阵
    T = [np.eye(4)]
    for i in range(1, 7):
        cos_theta = np.cos(theta[i])
        sin_theta = np.sin(theta[i])
        cos_alpha = np.cos(alpha[i])
        sin_alpha = np.sin(alpha[i])
        T.append(np.array([
            [cos_theta, -sin_theta*cos_alpha, sin_theta*sin_alpha, a[i]*cos_theta],
            [sin_theta , cos_theta * cos_alpha, -cos_theta*sin_alpha, sin_theta * a[i]],
            [0,  sin_alpha, cos_alpha, d[i]],
            [0, 0, 0, 1]
        ]))

    # 计算相对于基坐标的变换矩阵
    trans =  np.linalg.multi_dot(T[1:])
    #trans = np.dot(T[1], np.dot(T[2], np.dot(T[3], np.dot(T[4], np.dot(T[5], T[6])))))

    X=trans[0,3]
    Y=trans[1,3]
    Z=trans[2,3]


    return X,Y,Z


xs = []
ys = []
zs = []

# θ的随机样本
samples = np.random.uniform(low=-2*np.pi, high=2*np.pi, size=(100000, 7))

for sample in samples:
    x, y, z = fkr(sample)
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