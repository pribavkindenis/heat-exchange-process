import sys
from PyQt5.QtWidgets import QApplication
from app.app import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    exit(app.exec_())
