import tkinter as tk
from tkinter import messagebox
import subprocess

import os
import sys
# 获取当前脚本的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取parament.py所在的目录
parent_dir = os.path.dirname(current_dir)
# 将parament.py所在的目录添加到sys.path
sys.path.append(parent_dir)
# 导入parament.py
from parament import Para_Mana
pm=Para_Mana()#参数

class App:
    def __init__(self, root):
        self.pm = Para_Mana()
        self.root = root
        self.root.title("打印配置")

        # 创建并布局所有输入框和对应的保存按钮
        self.create_entry('a', '末端直线加速度', float)
        self.create_entry('v', '末端直线速度', float)
        self.create_entry('offset_x', '模型x坐标偏移', int)
        self.create_entry('offset_y', '模型y坐标偏移', int)
        self.create_entry('offset_z', '模型z坐标偏移', int)

        self.rollback_label = tk.Label(root, text="是否执行末端位姿回退矫正功能")
        self.rollback_var = tk.StringVar()
        self.rollback_var.set(self.pm.get_param('rollback'))
        self.rollback_option = tk.OptionMenu(root, self.rollback_var, 'y', 'n')

        self.start_button = tk.Button(root, text="开始打印",fg="#BA55D3",bg="#FFDAB9", command=self.start_print)

        self.rollback_label.pack()
        self.rollback_option.pack()
        self.start_button.pack()

    def create_entry(self, name, text, cast_type):
        label = tk.Label(self.root, text=f"{text}")
        entry = tk.Entry(self.root)
        entry.insert(0, self.pm.get_param(name))
        save_button = tk.Button(self.root, text="保存", command=lambda: self.pm.set_param(name, cast_type(entry.get())))

        label.pack()
        entry.pack()
        save_button.pack()

    def start_print(self):
        self.pm.set_param('rollback', self.rollback_var.get())
        # 将工作目录切换到脚本文件所在的目录
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        # 调用main.py
        subprocess.Popen(['python', 'main1.py'])
        messagebox.showinfo("打印配置", "开始打印")

root = tk.Tk()
# 设置窗口大小为300x200像素
root.geometry("300x500")

app = App(root)
root.mainloop()