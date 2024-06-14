import os
import sys
import shutil
import subprocess
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton, QMessageBox,QComboBox
from PyQt5.QtCore import Qt, pyqtSlot,QSize
from PyQt5.QtGui import QFont
from parament import Para_Mana
pm=Para_Mana()#参数

class App(QWidget):
    def __init__(self,pm):
        super().__init__()
        self.title = '机械臂切向3D打印过程'
        self.pm = pm
        self.initUI()

    def initUI(self):
        subprocess.Popen(['python', 'QTcmd.py'])
        self.setWindowTitle(self.title)
        vbox = QVBoxLayout()

        # 创建一个下拉列表（QComboBox）
        self.text_label = QLabel("输入路径手性旋向", self)
        vbox.addWidget(self.text_label)

        self.rot_option = QComboBox(self)
        # 创建一个QFont对象，并设置其字体大小
        font0 = QFont()
        font0.setFamily("Arial")  # 设置字体为Arial
        font0.setPointSize(8)  # 设置字体大小为8
        # 使用setFont()方法设置QComboBox的字体
        self.rot_option.setFont(font0)
        # 创建一个字典，键是选项的英文名，值是选项的中文名
        self.dic_ = {"left": "左旋", "right": "右旋"}
        # 遍历字典，将值作为选项添加到下拉列表中
        for i in self.dic_:
            self.rot_option.addItem(self.dic_[i])
            self.rot_option.resize(300, 80)
            self.rot_option.move(250, 50)
        self.rot_option.setCurrentText(self.pm.get_param('rot'))  # 设置初始选项
        self.rot_option.currentTextChanged.connect(self.change_rot)  # 连接到自定义槽函数
        vbox.addWidget(self.rot_option)


        self.label = QLabel('将需要被复制的文件拖放在这里', self)
        self.label.setAlignment(Qt.AlignCenter)
        font = QFont("Arial", 16)
        self.label.setFont(font)
        self.label.setStyleSheet("background-color: #E0FFFF; min-width: 600px; min-height: 400px")
        vbox.addWidget(self.label)

        self.button = QPushButton('删除txt文件', self)
        self.button.setStyleSheet("background-color: #FAEBD7; min-width: 20px; min-height: 40px")
        self.button.clicked.connect(self.delete)
        vbox.addWidget(self.button)

        # 创建直线打印按钮
        self.line_button = QPushButton("直线打印", self)
        self.line_button.setStyleSheet("background-color: #7FFFD4; min-width: 20px; min-height: 40px")
        self.line_button.clicked.connect(self.start_line_print)
        vbox.addWidget(self.line_button)

        # 创建曲线打印按钮
        self.curve_button = QPushButton("曲线打印", self)
        self.curve_button.setStyleSheet("background-color: #98FB98; min-width: 20px; min-height: 40px")
        self.curve_button.clicked.connect(self.start_curve_print)
        vbox.addWidget(self.curve_button)

        self.setLayout(vbox)

        self.show()

    def start_line_print(self):
        # 调用line/GUI.py
        subprocess.Popen(['python', 'line/GUI1QT.py'])
        QMessageBox.information(self, "打印配置", "开始直线打印")

    def start_curve_print(self):
        # 调用joint/GUI.py
        subprocess.Popen(['python', 'joint/GUI2QT.py'])
        QMessageBox.information(self, "打印配置", "开始曲线打印")

    def dropEvent(self, e):
        filepath = e.mimeData().urls()[0].toLocalFile()
        if filepath.endswith('.txt'):
            shutil.copy(filepath, './txt2csv/')
            QMessageBox.information(self, "文件复制", "TXT 文件已被复制到 txt2csv 目录")

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def change_rot(self, text):
        # 当下拉列表的当前选项改变时，更新'rot'参数
        self.pm.set_param('rot', text)

    def delete(self):
        folder = './txt2csv/'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) and file_path.endswith('.txt'):
                    os.unlink(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

        QMessageBox.information(self, "文件删除", " txt2csv 目录下的 TXT 文件已被删除")


if __name__ == '__main__':
    app = QApplication([])
    pm = Para_Mana()  # 创建一个Para_Mana实例
    ex = App(pm)
    app.exec_()