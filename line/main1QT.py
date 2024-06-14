from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt
import sys
import os
import subprocess


def run_script(script_path):
    print(f'正在运行: {script_path}')  # 添加这行来打印当前正在运行的脚本名称
    subprocess.check_call([sys.executable, script_path])


class ConfirmWindow(QWidget):
    def __init__(self, script_path):
        super().__init__()
        self.script_path = script_path
        self.initUI()

    def initUI(self):
        self.setWindowTitle('确认')
        self.setGeometry(800, 400, 500, 500)

        vbox = QVBoxLayout()

        self.yes_button = QPushButton('是', self)
        self.yes_button.clicked.connect(self.yes)
        self.no_button = QPushButton('否', self)
        self.no_button.clicked.connect(self.no)

        vbox.addWidget(self.yes_button)
        vbox.addWidget(self.no_button)

        self.setLayout(vbox)

    def yes(self):
        run_script(self.script_path)
        self.close()

    def no(self):
        print("已取消打印")
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 获取当前文件的绝对路径
    current_path = os.path.dirname(os.path.abspath(__file__))
    result = run_script('../txt2csv/if_model_inspace.py')
    if result == "No":
        confirm_window = ConfirmWindow('2makepose.py')
        confirm_window.show()
    else:
        run_script('2makepose.py')
        run_script('3normal.py')
        run_script('4euler.py')
        run_script('5simple_rdp.py')
        confirm_window = ConfirmWindow(os.path.join(current_path, 'goline.py'))
        confirm_window.show()

    sys.exit(app.exec_())