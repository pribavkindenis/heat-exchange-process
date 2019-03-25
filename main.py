import sys
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QWidget, QVBoxLayout, QSlider, QLabel
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from heat_process import HeatProcess


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.process = HeatProcess()

        self.figure = Figure()
        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvas(self.figure)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, self.process.t_batches)
        self.slider.valueChanged.connect(self.slider_change_handler)

        self.time_label = QLabel()
        self.time_label.setAlignment(Qt.AlignCenter)

        self.create_ui()
        self.slider_change_handler(0)

    def create_ui(self):
        v_box = QVBoxLayout()
        v_box.addWidget(self.canvas)
        v_box.addWidget(self.slider)
        v_box.addWidget(self.time_label)

        self.setLayout(v_box)
        self.setWindowTitle("Heat exchange process")
        self.setFixedHeight(self.sizeHint().height())
        self.setFixedWidth(800)
        self.center()

    def slider_change_handler(self, value):
        self.time_label.setText("t = {:.2f} s".format(self.process.ht * value))
        data = (self.process.x_range, self.process.u[value, :])
        self.plot(data, self.process.u0, self.get_color(value))

    def center(self):
        qt_rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

    def plot(self, data, u0, color):
        self.ax.clear()
        self.ax.plot(*data, color=color)
        self.ax.set_title("Temperature distribution")
        self.ax.set_ylabel("t, °C")
        self.ax.set_xlabel("x, cm")
        self.ax.grid()
        self.ax.set_ylim(u0 - 0.5, u0 + 1.5)
        self.canvas.draw()

    def get_color(self, value):
        t = 1 / self.process.t_batches
        return 1 - t*value, 0, t*value


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    exit(app.exec_())
