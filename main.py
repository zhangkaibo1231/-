import os
import shutil
import subprocess
import tkinter as tk
from tkinter import messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD

class App:
    def __init__(self, root):
        self.root = root
        self.label = tk.Label(self.root, text='将需要被复制的文件拖放在这里')
        self.label.pack(padx=100, pady=100)  # 设置拖放区域的大小

        self.button = tk.Button(self.root, text='删除txt文件', command=self.delete)
        self.button.pack()

        # 只有label区域接收拖放
        self.label.drop_target_register(DND_FILES)
        self.label.dnd_bind('<<Drop>>', self.drop)

    def start_line_print(self):
        # 调用line/GUI.py
        subprocess.Popen(['python', 'line/GUI.py'])
        messagebox.showinfo("打印配置", "开始直线打印")
        #self.root.destroy()  # 关闭窗口

    def start_curve_print(self):
        # 调用joint/GUI.py
        subprocess.Popen(['python', 'joint/GUI.py'])
        messagebox.showinfo("打印配置", "开始曲线打印")
        #self.root.destroy()  # 关闭窗口

    def drop(self, event):
        filepath = event.data
        if filepath.endswith('.txt'):
            shutil.copy(filepath, './txt2csv/')
            messagebox.showinfo("文件复制", "TXT 文件已被复制到 txt2csv 目录")

    def delete(self):
        folder = './txt2csv/'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) and file_path.endswith('.txt'):
                    os.unlink(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

        messagebox.showinfo("文件删除", " txt2csv 目录下的 TXT 文件已被删除")

root = TkinterDnD.Tk()
root.title('机械臂3D打印过程')
app = App(root)

# 创建直线打印按钮
line_button = tk.Button(root, text="直线打印", command=app.start_line_print)
line_button.pack()

# 创建曲线打印按钮
curve_button = tk.Button(root, text="曲线打印", command=app.start_curve_print)
curve_button.pack()

root.mainloop()