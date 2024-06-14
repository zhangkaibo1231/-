import asyncio
import lebai_sdk
import csv
import math

# 导入parament.py
from parament import Para_Mana
pm=Para_Mana()#参数

lebai_sdk.init()
##lebai.set_do("FLANGE", pin, value)设置法兰数字输出value:0/1,pin:0/1
##value = lebai.get_di("FLANGE", pin)获取法兰数字输入value:0/1,pin:0/1

async def main():
    # 加载末端位姿是否回退参数
    rollback_enabled = pm.get_param('rollback') == 'y'

    print(await lebai_sdk.discover_devices(2))  # 发现同一局域网内的机器人

    robot_ip = "10.20.17.1"  # 设定机器人ip地址，需要根据机器人实际ip地址修改
    lebai = await lebai_sdk.connect(robot_ip, False)  # 创建实例，False为实际控制
    await lebai.start_sys()  # 启动手臂
    lebai.set_tcp(pm.get_param('TCP'))#设置末端工具坐标系

    ##lebai.set_payload(2.0, {x=0, y=0, z=0.5})质量，重心位置，未测量

    initial_joints = await lebai.get_kin_data()#获取初始末端关节位姿
    initial_j6 = initial_joints['actual_joint_pose'][5]

    # 打开csv文件并读取位姿数据
    with open('simple_euler.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader, 1):  # 添加了enumerate函数，用于计数
            # 从csv文件的每一行中获取位姿数据
            cartesian_pose = {'x': float(row[0]), 'y': float(row[1]), 'z': float(row[2]), 'rz': float(row[3]),
                              'ry': float(row[4]), 'rx': float(row[5])}
            t = 0  # 运动时间 (s)。 当 t > 0 时，参数速度 v 和加速度 a 无效
            r = 0.001  # 交融半径 (m)。用于指定路径的平滑效果
            # 使用这些位姿数据来控制机械臂的运动
            await lebai.movel(cartesian_pose, pm.get_param('a'), pm.get_param('v'), t, r)

            current_joints =  await lebai.get_kin_data()  # 获取当前关节位置
            current_j6 =  await current_joints['actual_joint_pose'][5]  # 获取当前j6旋转角度

            # 每次读取一行就在3D图中添加一个点，并绘制一条从上一个点到这个点的线

            # 如果用户选择了进行末端角度回退，并且当前j6旋转角度大于相对于开始打印时的初始旋转角度大了2*pi
            if rollback_enabled and abs(current_j6 - initial_j6) > 2 * math.pi:
                # 暂停读取csv文件，并打印“末端位姿回退中”，机械臂停止运动
                print("末端位姿回退中")
                # 按照当前末端位姿坐标的Z轴负方向直线运动一定距离
                lebai.speedl(0.1, {'x': 0, 'y': 0, 'z': -0.05, 'rz': 0, 'ry': 0, 'rx': 0}, 0, {'x': float(row[0]), 'y': float(row[1]), 'z': float(row[2]), 'rz': float(row[3]), 'ry': float(row[4]), 'rx': float(row[5])})
                current_joints = await lebai.get_kin_data()  # 获取当前关节位置
                # 使得末端关节回退回初始旋转角度
                lebai.movej([current_joints['actual_joint_pose'][0],current_joints['actual_joint_pose'][1],current_joints['actual_joint_pose'][2]
                                      ,current_joints['actual_joint_pose'][3],current_joints['actual_joint_pose'][4],initial_j6], 0, math.pi/2, 0, 0)
                #回退位置
                lebai.speedl(0.1, {'x': 0, 'y': 0, 'z': 0.05, 'rz': 0, 'ry': 0, 'rx': 0}, 0, {'x': float(row[0]), 'y': float(row[1]), 'z': float(row[2]), 'rz': float(row[3]), 'ry': float(row[4]), 'rx': float(row[5])})

                continue

            print(f"当前已执行到第{i}行",'末端位姿:',current_j6)  # 打印当前执行到的行数
    await lebai.wait_move()  # 等待运动完成,速度降为0.
    await lebai.stop_sys()

asyncio.run(main())