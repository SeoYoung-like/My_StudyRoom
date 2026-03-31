import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QWidget

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("클래스 기반 윈도우")
        self.setGeometry(300, 300, 500, 400)

if __name__=="__main__":
    app = QApplication()
    window = MyWindow()
    window.show()
    sys.exit(app.exec())