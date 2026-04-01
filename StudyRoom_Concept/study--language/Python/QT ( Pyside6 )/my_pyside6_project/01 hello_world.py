import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QWidget

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("나의 첫 PySide6 프로그램")
window.setGeometry(100, 100, 400, 300)
window.show()

sys.exit(app.exec())