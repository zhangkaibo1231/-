import asyncio
import lebai_sdk
import math
import json

lebai_sdk.init()
##lebai.set_do("FLANGE", pin, value)设置法兰数字输出value:0/1,pin:0/1
##value = lebai.get_di("FLANGE", pin)获取法兰数字输入value:0/1,pin:0/1

async def main():

    print(await lebai_sdk.discover_devices(5))  # 发现同一局域网内的机器人,过程持续5s
    robot_ip = "10.20.17.1"  # 设定机器人ip地址，需要根据机器人实际ip地址修改
    lebai = await lebai_sdk.connect(robot_ip, False)  # 创建实例，False为实际控制
    await lebai.start_sys()  # 启动手臂
    ##lebai.set_payload(2.0, {x=0, y=0, z=0.5})末端质量，重心位置，未测量
    with open('print.json', 'r') as f:
        data = json.load(f)
        data_len=len(data)
        for i, module in enumerate(data, 1):  # 添加了enumerate函数，用于计数
            # 从json文件的每一单元中获取位姿数据
            joint_pose = module['theta']
            t = module['t']  # 运动时间 (s)。 当 t > 0 时，参数速度 v 和加速度 a 无效.
            await lebai.move_pt(joint_pose, t)
            print(f"当前已执行到第{i}/{data_len}行")  # 打印当前执行到的行数
    lebai.wait_move()
    lebai.stop_sys()

asyncio.run(main())