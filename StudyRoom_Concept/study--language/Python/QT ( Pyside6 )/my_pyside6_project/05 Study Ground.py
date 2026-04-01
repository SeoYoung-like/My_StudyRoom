import sys
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QApplication
from ui_my_window import Ui_Form


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.UIinit()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

    def UIinit(self):
        self.setWindowTitle("My윈도우 - TEST")
        self.setGeometry(100, 100, 800, 500)


app = QApplication(sys.argv)
my_window = MyWindow()
my_window.show()

sys.exit(app.exec())