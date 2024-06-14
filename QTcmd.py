import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton

class ConsoleOutput(QTextEdit):
    def write(self, text):
        self.insertPlainText(text)

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.output = ConsoleOutput()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('控制台输出')
        self.setGeometry(400, 400, 800, 600)

        vbox = QVBoxLayout()
        vbox.addWidget(self.output)

        self.setLayout(vbox)

    def print_console(self):
        print("控制台输出重新定位>>>")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    ex.output.setStyleSheet("font-size: 28px")
    sys.stdout = ex.output#控制台输出重新定位
    ex.print_console()
    sys.exit(app.exec_())