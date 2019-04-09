import sys
from PyQt5.QtWidgets import QApplication
import application

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = application.MainWindow()
    main_window.show()
    exit(app.exec_())
