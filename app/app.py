from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from typing import *
from enum import Enum

from app.process.numerically_calculated_process import NumericallyCalculatedProcess
from app.process.explicitly_calculated_process import ExplicitlyCalculatedProcess
from app.process.inexplicitly_calculated_process import InexplicitlyCalculatedProcess
from app.process.analytically_calculated_process import AnalyticallyCalculatedProcess


class MainWindow(QWidget):
    figure: Figure
    ax: Axes
    canvas: FigureCanvas

    scheme_type_box: QComboBox
    show_analytical: QCheckBox
    slider: QSlider
    time_label: QLabel

    l_edit: QLineEdit
    t_edit: QLineEdit
    s_edit: QLineEdit
    a_edit: QLineEdit
    k_edit: QLineEdit
    c_edit: QLineEdit
    u0_edit: QLineEdit
    x_num_edit: QLineEdit
    t_num_edit: QLineEdit
    eps_edit: QLineEdit

    restore_defaults_btn: QPushButton

    analytical: Optional[AnalyticallyCalculatedProcess]
    numerical: Optional[NumericallyCalculatedProcess]

    successfully_parsed: bool
    params: List[float or int]
    editors: List[QLineEdit]

    thread: QThread

    def __init__(self):
        super().__init__()
        self.default_editor_style = ""
        self.danger_editor_style = "color:white;background-color:#ff4747"
        self.create_widgets()
        self.set_defaults()
        self.create_ui()
        self.params_change_handler()

    def params_change_handler(self):
        self.parse_parameters()
        self.analytical = None
        self.numerical = None
        self.remove_tooltips()
        if self.successfully_parsed:
            def calculate():
                self.numerical = self.create_numerical()
                self.add_tooltips()
                if self.show_analytical.isChecked():
                    self.analytical = self.create_analytical()
                return self
            self.update_slider_range()
            self.start_calculation_thread(calculate)

    def scheme_type_change_handler(self):
        def calculate():
            self.numerical = self.create_numerical()
            self.add_tooltips()
            return self
        self.numerical = None
        self.remove_tooltips()
        self.start_calculation_thread(calculate)

    def show_analytical_change_handler(self, state):
        if state == Qt.Checked and self.analytical is None:
            def calculate():
                self.analytical = self.create_analytical()
                return self
            self.start_calculation_thread(calculate)
        else:
            self.finish_change_handling()

    def start_calculation_thread(self, calculate: Callable):
        self.thread = self.CalculationThread(calculate)
        self.thread.calculated.connect(self.finish_change_handling)
        self.draw_loading()
        self.set_ui_enabled(False)
        self.thread.start()

    def finish_change_handling(self):
        self.set_ui_enabled(True)
        self.slider.setValue(0)
        self.slider_change_handler(0)
        self.eps_edit.setEnabled(self.show_analytical.isChecked())

    def slider_change_handler(self, index):
        t = self.numerical.get_tn()
        self.time_label.setText("Текущее время: {:.2f} c".format(t[index]))
        self.draw_plot(index)

    def add_tooltips(self):
        self.x_num_edit.setToolTip("При текущих параметрах желательно как максимум {}"
                                   .format(self.numerical.get_max_x_num()))
        self.t_num_edit.setToolTip("При текущих параметрах желательно как минимум {}"
                                   .format(self.numerical.get_min_t_num()))

    def remove_tooltips(self):
        self.x_num_edit.setToolTip("")
        self.t_num_edit.setToolTip("")

    def update_slider_range(self):
        self.slider.setRange(0, self.get_t_num() - 1)

    def create_analytical(self):
        (l, t, s, a, k, c, u0, x_num, t_num, eps) = self.params
        phi: Callable = lambda x: 0
        xi: Callable = lambda x: -4 * x ** 2 / l ** 2 + 4 * x / l + u0
        return AnalyticallyCalculatedProcess(l, t, s, a, k, c, u0, phi, xi, x_num, t_num, eps)

    def create_numerical(self) -> NumericallyCalculatedProcess:
        scheme_type = self.get_current_scheme_type()
        if scheme_type == self.SchemeType.EXPLICIT:
            return self.create_explicit()
        elif scheme_type == self.SchemeType.INEXPLICIT:
            return self.create_inexplicit()

    def get_current_scheme_type(self):
        index = self.scheme_type_box.currentIndex()
        return self.scheme_type_box.model().item(index).data()

    def create_explicit(self) -> ExplicitlyCalculatedProcess:
        (l, t, s, a, k, c, u0, x_num, t_num, eps) = self.params
        phi: Callable = lambda x: 0
        xi: Callable = lambda x: -4 * x ** 2 / l ** 2 + 4 * x / l + u0
        return ExplicitlyCalculatedProcess(l, t, s, a, k, c, u0, phi, xi, x_num, t_num)

    def create_inexplicit(self) -> InexplicitlyCalculatedProcess:
        (l, t, s, a, k, c, u0, x_num, t_num, eps) = self.params
        phi: Callable = lambda x: 0
        xi: Callable = lambda x: -4 * x ** 2 / l ** 2 + 4 * x / l + u0
        return InexplicitlyCalculatedProcess(l, t, s, a, k, c, u0, phi, xi, x_num, t_num)

    def draw_loading(self):
        self.ax.clear()
        self.ax.axis("off")
        self.ax.text(0.5, 0.5, "Выполняется вычисление...", va="center", ha="center", fontsize=15)
        self.canvas.draw()

    def draw_plot(self, index):
        self.ax.clear()
        self.ax.axis("on")
        x = self.numerical.get_xn()
        y = self.numerical.get_solution(index)
        self.ax.plot(x, y, color="purple", linewidth=2.0)

        if self.show_analytical.isChecked():
            x = self.analytical.get_xn()
            y = self.analytical.get_solution(index)
            self.ax.plot(x, y, color="orange", linestyle="--", linewidth=2.0)

        u0 = self.get_u0()
        self.ax.set_ylim(u0 - 0.5, u0 + 1.5)
        self.ax.set_title("График распределения температуры")
        self.ax.set_ylabel("t, °C")
        self.ax.set_xlabel("x, см")
        self.ax.grid()
        self.canvas.draw()

    def parse_parameters(self):
        params = []
        try:
            error_found = False

            for i in range(len(self.editors)):
                cast_func = float
                if i == 7 or i == 8:  # x_num and t_num params
                    cast_func = int
                editor = self.editors[i]
                if editor.hasAcceptableInput():
                    params.append(cast_func(editor.text()))
                    editor.setStyleSheet(self.default_editor_style)
                else:
                    editor.setStyleSheet(self.danger_editor_style)
                    error_found = True

            if error_found:
                raise ValueError()
        except ValueError:
            self.successfully_parsed = False
            self.set_widgets_enabled(False)
        else:
            self.params = params
            self.successfully_parsed = True
            self.set_widgets_enabled(True)

    def set_widgets_enabled(self, trigger):
        self.show_analytical.setEnabled(trigger)
        self.slider.setEnabled(trigger)
        self.scheme_type_box.setEnabled(trigger)

    def set_ui_enabled(self, trigger):
        self.set_widgets_enabled(trigger)
        self.restore_defaults_btn.setEnabled(trigger)
        for i in range(len(self.editors)):
            self.editors[i].setEnabled(trigger)

    def get_u0(self) -> float:
        return self.params[6]

    def get_t_num(self) -> int:
        return self.params[8]

    def create_widgets(self):
        self.figure = Figure()
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)

        self.scheme_type_box = QComboBox()
        self.show_analytical = QCheckBox()

        self.editors = []

        self.l_edit = QLineEdit()
        self.t_edit = QLineEdit()
        self.s_edit = QLineEdit()
        self.a_edit = QLineEdit()
        self.k_edit = QLineEdit()
        self.c_edit = QLineEdit()
        self.u0_edit = QLineEdit()
        self.x_num_edit = QLineEdit()
        self.t_num_edit = QLineEdit()
        self.eps_edit = QLineEdit()

        self.editors.append(self.l_edit)
        self.editors.append(self.t_edit)
        self.editors.append(self.s_edit)
        self.editors.append(self.a_edit)
        self.editors.append(self.k_edit)
        self.editors.append(self.c_edit)
        self.editors.append(self.u0_edit)
        self.editors.append(self.x_num_edit)
        self.editors.append(self.t_num_edit)
        self.editors.append(self.eps_edit)

        self.slider = QSlider(Qt.Horizontal)
        self.time_label = QLabel()
        self.restore_defaults_btn = QPushButton()

    def set_defaults(self):
        self.l_edit.setText(str(10))
        self.t_edit.setText(str(50))
        self.s_edit.setText(str(0.01))
        self.a_edit.setText(str(0.005))
        self.k_edit.setText(str(0.65))
        self.c_edit.setText(str(1.84))
        self.u0_edit.setText(str(20))
        self.x_num_edit.setText(str(55))
        self.t_num_edit.setText(str(3000))
        self.eps_edit.setText(str(0.01))

    def create_ui(self):
        grid = QGridLayout()
        grid.setSpacing(10)

        explicit_item = QStandardItem("Явная разностная схема")
        explicit_item.setData(self.SchemeType.EXPLICIT)
        self.scheme_type_box.model().appendRow(explicit_item)

        inexplicit_item = QStandardItem("Невная разностная схема")
        inexplicit_item.setData(self.SchemeType.INEXPLICIT)
        self.scheme_type_box.model().appendRow(inexplicit_item)

        self.show_analytical.setText("Наложить аналитическое решение")

        self.time_label.setAlignment(Qt.AlignCenter)

        self.restore_defaults_btn.setText("Восстановить значения по умолчанию")

        self.scheme_type_box.currentIndexChanged.connect(self.scheme_type_change_handler)
        self.show_analytical.stateChanged.connect(self.show_analytical_change_handler)
        self.slider.valueChanged.connect(self.slider_change_handler)
        self.restore_defaults_btn.clicked.connect(self.set_defaults)

        grid.addWidget(self.canvas, 0, 0, 5, 1)
        grid.addWidget(self.scheme_type_box, 0, 1)
        grid.addWidget(self.show_analytical, 1, 1)
        grid.addLayout(self.create_form_layout(), 2, 1)
        grid.addWidget(self.restore_defaults_btn, 3, 1)
        grid.addWidget(self.time_label, 4, 1)
        grid.addWidget(self.slider, 5, 0, 1, 2)

        self.setLayout(grid)
        self.setWindowTitle("Процесс теплообмена в тонком стержне")
        self.setFixedHeight(self.sizeHint().height())
        self.setFixedWidth(1050)
        self.center()

    def create_form_layout(self) -> QFormLayout:
        form = QFormLayout()

        double_validator = self.DoubleValidator()
        double_validator.setLocale(QLocale(QLocale.English))
        double_validator.setBottom(0)

        int_validator = QIntValidator()
        int_validator.setBottom(2)

        timer = QTimer()
        timer.setSingleShot(True)
        timer.setInterval(300)
        timer.timeout.connect(self.params_change_handler)
        text_changed_handler: Callable = lambda: timer.start()

        self.setup_line_edit(self.l_edit, double_validator, text_changed_handler)
        form.addRow("Длина стержня", self.l_edit)

        self.setup_line_edit(self.t_edit, double_validator, text_changed_handler)
        form.addRow("Граница временного интервала", self.t_edit)

        self.setup_line_edit(self.s_edit, double_validator, text_changed_handler)
        form.addRow("Площадь поперечного сечения", self.s_edit)

        self.setup_line_edit(self.a_edit, double_validator, text_changed_handler)
        form.addRow("Коэффициент теплообмена", self.a_edit)

        self.setup_line_edit(self.k_edit, double_validator, text_changed_handler)
        form.addRow("Коэффициент теплопроводности", self.k_edit)

        self.setup_line_edit(self.c_edit, double_validator, text_changed_handler)
        form.addRow("Коэффициент объёмной теплоёмкости", self.c_edit)

        self.setup_line_edit(self.u0_edit, double_validator, text_changed_handler)
        form.addRow("Температура окружающей среды", self.u0_edit)

        self.setup_line_edit(self.x_num_edit, int_validator, text_changed_handler)
        form.addRow("Количество разбиений по x", self.x_num_edit)

        self.setup_line_edit(self.t_num_edit, int_validator, text_changed_handler)
        form.addRow("Количество разбиений по t", self.t_num_edit)

        self.setup_line_edit(self.eps_edit, double_validator, text_changed_handler)
        form.addRow("Точность аналитического решения", self.eps_edit)

        return form

    @staticmethod
    def setup_line_edit(line_edit: QLineEdit, validator: QValidator, handler: Callable):
        line_edit.setValidator(validator)
        line_edit.textChanged.connect(handler)

    def center(self):
        qt_rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

    class CalculationThread(QThread):
        calculated = pyqtSignal(object)

        def __init__(self, calculate: Callable):
            super().__init__()
            self.calculate = calculate

        def run(self) -> None:
            self.calculated.emit(self.calculate())

    class DoubleValidator(QDoubleValidator):
        def validate(self, p_str, p_int):
            return super().validate(p_str.replace(",", "."), p_int)

    class SchemeType(Enum):
        EXPLICIT = 1
        INEXPLICIT = 2
