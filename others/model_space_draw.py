import numpy as np
from math import *
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt

ang=[1,2,1,1,0,1]

def RotationMatrix(i,ang):
    d = [0, 0.216363, 0, 0, 0.119808, 0.098406, 0.083254]
    a = [0, 0, -0.280793, -0.259692, 0, 0, 0]
    alpha = [0, np.pi / 2, 0, 0, np.pi / 2, -np.pi / 2, 0]  # lebai 机器人的alpha参数（以弧度为单位）
    # theta = np.zeros(7)  # 每个关节的角度位置
    # theta[1], theta[2], theta[3], theta[4], theta[5], theta[6] = [float(val) for val in input("请输入各关节角度 1, 2, 3, 4, 5, 6:\n").split()]
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
            transform = np.linalg.multi_dot(T[1:i + 1])
            trans.append(transform)

    return trans[i]

class Target(object):

    def __init__(self, trans, radius, length, position_x, position_y, position_z, **kwargs):
        self.radius = radius#半径
        self.trans = np.array(trans)#旋转矩阵
        self.length = length#长度
        self.position = [position_x, position_y, position_z]#位置


def show_cylinder(fig, targets):
    """在3D坐标轴下展示一个任意位置，任意姿态的圆柱体
    Parameters
    ----------
    fig : matplotlib.figure.Figure
        传入一个空白的fig
    target : class Target
        一个圆柱体
    """
    fig.clf()  # 清除不同检测场景中的图形
    # 显示圆柱体
    ax = fig.add_subplot(projection='3d')
    ax.view_init(30, 45)#初始视角
    ax.set_xticks(np.arange(-2, 2, 0.2))#坐标范围
    ax.set_yticks(np.arange(-2, 2, 0.2))
    ax.set_xlabel('X/m')#刻度
    ax.set_ylabel('Y/m')
    ax.set_zlabel('Z/m')
    ax.set_xlim(-2, 2)#显示范围
    ax.set_ylim(-2, 2)

    for target in targets:
        a = target.trans
        u = np.linspace(0, 2 * np.pi, 50)  # 把圆划分50等份
        h = np.linspace(-0.5, 0.5, 2)  # 把高(1m)划分两等份,对应上底和下底

        x = target.radius * np.sin(u)
        y = target.radius * np.cos(u)

        x = np.outer(x, np.ones(len(h)))  # 20*2
        y = np.outer(y, np.ones(len(h)))  # 20*2
        z = np.outer(np.ones(len(u)), h)  # 20*2
        z = z * target.length

        x_rotation = np.ones(x.shape)  # 旋转后的坐标 20*2
        y_rotation = np.ones(y.shape)
        z_rotation = np.ones(z.shape)

        #a = target(trans[i][:3,:3])  # 3*3 pitch,roll
        #a = np.array(RotationMatrix(2, 1, 3, 4, 5, 6, 7))  # 3*3 pitch,roll

        for i in range(2):
            r = np.c_[x[:, i], y[:, i], z[:, i]]  # 20*3
            rT = r @ a  # 20*3
            x_rotation[:, i] = rT[:, 0]
            y_rotation[:, i] = rT[:, 1]
            z_rotation[:, i] = rT[:, 2]

        ax.plot_surface(x_rotation + target.position[0], y_rotation + target.position[1],
                        z_rotation + target.position[2],
                        color='#E7C261', alpha=1, antialiased=False)

        verts = [list(zip(x_rotation[:, 0] + target.position[0], y_rotation[:, 0] + target.position[1],
                          z_rotation[:, 0] + target.position[2]))]

        ax.add_collection3d(Poly3DCollection(verts, facecolors='#E7C261'))
        verts = [list(zip(x_rotation[:, 1] + target.position[0], y_rotation[:, 1] + target.position[1],
                          z_rotation[:, 1] + target.position[2]))]

        ax.add_collection3d(Poly3DCollection(verts, facecolors='#E7C261'))
        ax.grid(None)  # 删除背景网格\

    ax.set_zlim(min(target.position[2] for target in targets) - 2, 0.1)




trans0 = RotationMatrix(0, ang)
trans1 = RotationMatrix(1, ang)
trans2 = RotationMatrix(2, ang)
trans3 = RotationMatrix(3, ang)
trans4 = RotationMatrix(4, ang)
trans5 = RotationMatrix(5, ang)
trans6 = RotationMatrix(6, ang)

#具体有待修改
target0 = Target(trans0[:3,:3], 0.05,0.21583 , 0, 0, 0)
target1 = Target(-trans1[:3,:3], 0.025, 0.09, float(trans1[0,3]), float(trans1[1,3]), float(trans1[2,3]))
target2 = Target(trans2[:3,:3], 0.025, 0.28, float(trans2[0,3]), float(trans2[1,3]), float(trans2[2,3]))
target3 = Target(trans3[:3,:3], 0.025, 0.26, float(trans3[0,3]), float(trans3[1,3]), float(trans3[2,3]))
target4 = Target(-trans4[:3,:3], 0.025, 0.12063, float(trans4[0,3]), float(trans4[1,3]), float(trans4[2,3]))
target5 = Target(-trans5[:3,:3], 0.025, 0.09833, float(trans5[0,3]), float(trans5[1,3]), float(trans5[2,3]))
target6= Target(trans6[:3,:3], 0.025, 0.08343, float(trans6[0,3]), float(trans6[1,3]), float(trans6[2,3]))
tools= Target(trans6[:3,:3], 0.005, 0.118, float(trans6[0,3]), float(trans6[1,3]), float(trans6[2,3]))

fig = plt.figure()
show_cylinder(fig, [target0,target1,target2,target3,target4,target5,target6,tools])

plt.show()
