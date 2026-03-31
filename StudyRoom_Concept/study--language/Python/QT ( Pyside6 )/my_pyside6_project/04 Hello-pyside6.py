import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QWidget
from ui_my_window import Ui_Form

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.UI = Ui_Form()
        self.UI.setupUi(self)

    def initUI(self):
        self.setWindowTitle("Hello PySide6")
        self.setGeometry(100, 100, 800, 600)
        
if __name__=="__main__":
    app = QApplication()
    screen = QApplication.primaryScreen().geometry()
        
    window = MyWindow()
    x = (screen.width() - window.width()) // 2
    y = (screen.height() - window.height()) // 2
    window.move(x, y)

    window.show()
    

    sys.exit(app.exec())


