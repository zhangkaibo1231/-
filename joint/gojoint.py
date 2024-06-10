import asyncio
import lebai_sdk
import math
import json
# import nest_asyncio
# nest_asyncio.apply()


lebai_sdk.init()
##lebai.set_do("FLANGE", pin, value)设置法兰数字输出value:0/1,pin:0/1
##value = lebai.get_di("FLANGE", pin)获取法兰数字输入value:0/1,pin:0/1
async def move_pt(lebai, joint_pose, t):
    await lebai.move_pt(joint_pose, t)
    print(f"move_pt completed with {joint_pose}")

async def main():

    print(await lebai_sdk.discover_devices(5))  # 发现同一局域网内的机器人,过程持续5s

    robot_ip = "10.20.17.1"  # 设定机器人ip地址，需要根据机器人实际ip地址修改
    lebai = await lebai_sdk.connect(robot_ip, False)  # 创建实例，False为实际控制

    await lebai.start_sys()  # 启动手臂
    tasks=[]# 存储所有的运动任务

    ##lebai.set_payload(2.0, {x=0, y=0, z=0.5})末端质量，重心位置，未测量

    # 打开csv文件并读取位姿数据
    with open('print.json', 'r') as f:
        data = json.load(f)
        data_len=len(data)
        for i, module in enumerate(data, 1):  # 添加了enumerate函数，用于计数
            # 从csv文件的每一行中获取位姿数据
            joint_pose = module['theta']
            #a=0#主轴加速度
            #v=0#主轴转速
            t = module['t'] # 运动时间 (s)。 当 t > 0 时，参数速度 v 和加速度 a 无效
            r = 0  # 交融半径 (m)。用于指定路径的平滑效果

            # 创建一个运动任务，并将其添加到任务列表中
            task = move_pt(lebai, joint_pose, t)
            tasks.append(asyncio.ensure_future(task))
            # 使用这些位姿数据来控制机械臂的运动
            #await lebai.movej(joint_pose, a, v, t, r)
            #await lebai.move_pt(joint_pose,t)
            #await lebai.wait_move()
            print(f"当前已执行到第{i}/{data_len}行")  # 打印当前执行到的行数

    # 使用gather来等待所有的运动任务完成
    await asyncio.gather(*tasks)
    await lebai.stop_sys()

asyncio.run(main())