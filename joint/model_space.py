import numpy as np

#point = [float(val) for val in input("请输入点的坐标:\n").split()]
#theta = np.zeros(6)  # 每个关节的角度位置
#theta[0], theta[1], theta[2], theta[3], theta[4], theta[5] = [float(val) for val in input("请输入各关节角度 1, 2, 3, 4, 5, 6:\n").split()]

def model_space(ang,point):
    d = [0, 0.216363, 0, 0, 0.119808, 0.098406, 0.083254]
    a = [ 0, 0, -0.280793, -0.259692, 0, 0,0]
    alpha = [0, np.pi / 2, 0, 0, np.pi / 2, -np.pi / 2, 0]  # lebai 机器人的alpha参数（以弧度为单位）

    # 计算关节之间的变换矩阵
    T = [np.eye(4)]
    T[0]=np.eye(4)
    ang = np.array(ang)  # 把输入参数转换为numpy数组
    theta = np.insert(ang, 0, 0)  # 在index为0的位置插入0
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

    class CylinderRegion:  # 定义圆柱体空间
        def __init__(self, axis_length, radius, base_center, axis_direction):
            self.axis_length = axis_length
            self.radius = radius
            self.base_center = np.array(base_center).astype(float)
            self.axis_direction = np.array(axis_direction) / np.linalg.norm(axis_direction)  # 归一化方向向量
        def is_point_inside(self, point):
            # 将点转换为 numpy 数组
            point = np.array(point).astype(float)
            # 计算从基中心到点的向量
            vec = point[:3] - self.base_center
            # 将此向量投影到轴方向上
            proj = np.dot(vec, self.axis_direction)
            # 如果投影超出范围 [0， axis_length]，则该点位于圆柱体之外
            if proj < 0 or proj > self.axis_length:
                return False
            # 计算从点到圆柱轴线的距离
            dist_to_axis = np.linalg.norm(vec - proj * self.axis_direction)
            # 如果此距离大于半径，则该点位于圆柱体外部
            if dist_to_axis > self.radius:
                return False
            # 否则，该点位于圆柱体内部
            return True

    # 考虑实际模型，且与关节角度关联的圆柱体近似机械臂模型空间
    ax0 = CylinderRegion(axis_length=d[1], radius=0.05, base_center=[0, 0, 0], axis_direction=[0, 0, 1])
    ax1 = CylinderRegion(axis_length=-0.09, radius=0.025, base_center=[trans[1][0, 3], trans[1][1, 3], trans[1][2, 3]],
                         axis_direction=[trans[1][0, 1], trans[1][1, 1], trans[1][2, 1]])
    ax2 = CylinderRegion(axis_length=-a[2], radius=0.025,
                         base_center=[trans[2][0, 3], trans[2][1, 3], (trans[2][2, 3] + 0.1)],
                         axis_direction=[trans[2][0, 0], trans[2][1, 0], trans[2][2, 0]])
    ax3 = CylinderRegion(axis_length=-a[3], radius=0.025,
                         base_center=[trans[3][0, 3], trans[3][1, 3], (trans[3][2, 3] + 0.02)],
                         axis_direction=[trans[3][0, 0], trans[3][1, 0], trans[3][2, 0]])
    ax4 = CylinderRegion(axis_length=-d[4], radius=0.025, base_center=[trans[4][0, 3], trans[4][1, 3], trans[4][2, 3]],
                         axis_direction=[trans[4][0, 2], trans[4][1, 2], trans[4][2, 2]])
    ax5 = CylinderRegion(axis_length=-d[5], radius=0.025, base_center=[trans[5][0, 3], trans[5][1, 3], trans[5][2, 3]],
                         axis_direction=[trans[5][0, 2], trans[5][1, 2], trans[5][2, 2]])
    ax6 = CylinderRegion(axis_length=-d[6], radius=0.025, base_center=[trans[6][0, 3], trans[6][1, 3], trans[6][2, 3]],
                         axis_direction=[trans[6][0, 2], trans[6][1, 2], trans[6][2, 2]])
    tools = CylinderRegion(axis_length=0.118, radius=0.015,
                           base_center=[trans[6][0, 3], trans[6][1, 3], trans[6][2, 3]],
                           axis_direction=[trans[6][0, 2], trans[6][1, 2], trans[6][2, 2]])
    def check_interference(point):
        cylinders = [ax0, ax1, ax2, ax3, ax4, ax5, ax6, tools]
        for cylinder in cylinders:
            if cylinder.is_point_inside(point):
                return "no"  # 干涉
        return "yes"  #不干涉

    end=check_interference(point)

    return end


#model_space(theta,point)
#print(model_space(theta,point))




