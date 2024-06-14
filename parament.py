class Para_Mana:
    def __init__(self):
        self.params = {
            'a':0.01,#设置参数a:末端直线加速度
            'v':0.04,#v:末端直线速度m/s
            'offset_x':0,#模型坐标偏移
            'offset_y':200,
            'offset_z':0,
            'rollback':'y',#是否执行末端位姿重置，y表示同意
            'TCP':{"x": 0.001,"y": 0,"z": 0.118,"rz": 0,"ry": 0,"rx": 0},
            'epsilon':0.0001,#RDP算法简化阈值
            's':5,#空间点模型简化间隔
            'n':10,#碰撞检测误差缓冲
            'm':6,#换行处两侧去除点数
            'weight':[1.25, 1.15, 1.05, 0.95, 0.85, 0.75],#各关节选择加权比重theta1-theta6,默认[1.25,1.15,1.05,1.5,1.5,0.75]
            'we5':0.5,#规避腕部奇异点系数
            'rot':'left'#使用UG提取铣削轨迹(自下而上)时的旋转方向，默认为left，代表左手螺旋
                       }

    def add_param(self, name, value):#设置参数
        self.params[name] = value

    def set_param(self, name, value):#修改参数
        if name in self.params:
            self.params[name] = value
        else:
            raise ValueError(f"Parameter '{name}' does not exist")

    def get_param(self, name):#引用参数
        return self.params.get(name, None)
