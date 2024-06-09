class Para_Mana:
    def __init__(self):
        self.params = {
            'a':0.01,#设置参数a:末端直线加速度
            'v':0.06,#v:末端直线速度m/s
            'offset_x':-260,#模型坐标偏移
            'offset_y':0,
            'offset_z':200,
            'rollback':'y',#是否执行末端位姿重置，y表示同意
            'TCP':{"x": 0.001,"y": 0,"z": 0.118,"rz": 0,"ry": 0,"rx": 0}
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