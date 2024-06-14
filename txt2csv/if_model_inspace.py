import math
import pandas as pd
import glob
from txt2csv.txtend import datamake
from parament import Para_Mana
pm=Para_Mana()#参数
offsets = [pm.get_param('offset_x'), pm.get_param('offset_y'), pm.get_param('offset_z')]
files = glob.glob('*.txt')
data = datamake(offsets,files)
data = pd.DataFrame(data)
data = data.apply(pd.to_numeric, errors='coerce')

def if_model_in_space(data):
    def is_point_in_space(point):  # 机械臂灵活工作空间
        x, y, z = point
        radius_sphere = 540
        radius_cylinder = 340 / 2
        distance_to_origin = math.sqrt(x ** 2 + y ** 2 + z ** 2)
        if distance_to_origin > radius_sphere:
            return False
        distance_to_z_axis = math.sqrt(x ** 2 + y ** 2)
        if distance_to_z_axis < radius_cylinder:
            return False
        return True

    def process_data(data):
        for index, row in data.iterrows():
            point = [float(i) for i in row[:3]]  # 假设DataFrame中的每一行的前三列是点的x,y,z坐标
            if not is_point_in_space(point):
                return "No"  # 如果有一个点不在空间内，就立即返回"No"
        return "Yes"  # 如果所有点都在空间内，就返回"Yes"

    return print(process_data(data))

if_model_in_space(data)