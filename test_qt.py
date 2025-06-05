from PyQt5.QtWidgets import QApplication, QLabel
import sys
app = QApplication(sys.argv)
label = QLabel('Test PyQt5')
label.show()
app.exec_()