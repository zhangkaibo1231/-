from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QComboBox,QMessageBox
from PyQt5.QtCore import Qt
import sys
from parament import Para_Mana
import os
import subprocess

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.pm = Para_Mana()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('打印配置')
        self.setGeometry(800, 400, 400, 400)

        vbox = QVBoxLayout()
        self.create_entry(vbox, 'offset_x', '模型x坐标偏移', int)
        self.create_entry(vbox, 'offset_y', '模型y坐标偏移', int)
        self.create_entry(vbox, 'offset_z', '模型z坐标偏移', int)
        start_button = QPushButton('开始打印', self)
        start_button.setStyleSheet("background-color: #FFDAB9; color: #BA55D3")
        start_button.clicked.connect(self.start_print)
        vbox.addWidget(start_button)
        self.setLayout(vbox)

    def create_entry(self, vbox, name, text, cast_type):
        label = QLabel(text)
        entry = QLineEdit()
        entry.setText(str(self.pm.get_param(name)))
        save_button = QPushButton('保存')
        save_button.clicked.connect(lambda: self.pm.set_param(name, cast_type(entry.text())))
        vbox.addWidget(label)
        vbox.addWidget(entry)
        vbox.addWidget(save_button)

    def start_print(self):
        # 将工作目录切换到脚本文件所在的目录
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        # 调用main.py
        subprocess.Popen(['python', 'main2QT.py'])
        # 创建一个信息消息对话框
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("打印配置")
        msgBox.setText("开始打印")
        msgBox.exec()

def main():
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()