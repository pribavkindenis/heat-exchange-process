from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from typing import *
from enum import Enum
import numpy as np

from app.util import SchemeType, create_analytical, create_numerical

from app.process.numerically_calculated_process import NumericallyCalculatedProcess
from app.process.analytically_calculated_process import AnalyticallyCalculatedProcess


class ConvergenceReport(QWidget):

    DEFAULT_STYLE = ""
    DANGER_STYLE = "color:white;background-color:#ff4747"

    table: QTableWidget

    progress_bar: QProgressBar
    iterations_num_label: QLabel
    iterations_num_edit: QLineEdit
    start_btn: QPushButton
    close_btn: QPushButton

    close_handler: Callable

    iterations_num: int
    progress_bar_step: int

    x_scale: int
    t_scale: int

    def __init__(self, params: List[float or int], scheme_type: SchemeType):
        super().__init__()
        self.columns_num = 9
        self.params = params
        self.scheme_type = scheme_type
        self.create_ui()
        self.set_defaults()
        self.configure_ui()
        self.set_layout(self.FooterLayout.INIT)

    def start_convergence_report(self):
        self.set_layout(self.FooterLayout.PROGRESS)
        self.init_report_params()

        analytical = create_analytical(self.params)
        numerical = create_numerical(self.scheme_type, self.params)
        error: float = self.get_calculation_error(analytical, numerical)
        self.create_row(0, numerical, error, first_row=True)
        prev_hx = numerical.get_hx()
        prev_ht = numerical.get_ht()
        prev_error = error
        self.update_progress_bar()

        for i in range(1, self.iterations_num):
            self.params[7] *= self.x_scale
            self.params[8] *= self.t_scale
            analytical = create_analytical(self.params)
            numerical = create_numerical(self.scheme_type, self.params)
            error: float = self.get_calculation_error(analytical, numerical)
            self.create_row(i, numerical, error, prev_hx, prev_ht, prev_error)
            prev_hx = numerical.get_hx()
            prev_ht = numerical.get_ht()
            prev_error = error
            self.update_progress_bar()

        self.set_layout(self.FooterLayout.FINAL)

    def create_row(self,
                   row_index: int,
                   numerical: NumericallyCalculatedProcess,
                   error: float,
                   prev_hx: float = None,
                   prev_ht: float = None,
                   prev_error: float = None,
                   first_row: bool = False):
        first_col = QTableWidgetItem(str(row_index + 1))
        second_col = QTableWidgetItem(str(numerical.get_x_num()))
        third_col = QTableWidgetItem(str(numerical.get_t_num()))
        fourth_col = QTableWidgetItem(self.pretty_double(numerical.get_hx()))
        fifth_col = QTableWidgetItem(self.pretty_double(numerical.get_ht()))
        sixth_col = QTableWidgetItem(self.pretty_double(error))
        if not first_row:
            seventh_col = QTableWidgetItem(str(int(prev_hx / numerical.get_hx())))
            eighth_col = QTableWidgetItem(str(int(prev_ht / numerical.get_ht())))
            ninth_col = QTableWidgetItem(self.pretty_double(prev_error / error))
        else:
            seventh_col = QTableWidgetItem("-")
            eighth_col = QTableWidgetItem("-")
            ninth_col = QTableWidgetItem("-")

        self.table.insertRow(self.table.rowCount())
        self.table.setItem(row_index, 0, first_col)
        self.table.setItem(row_index, 1, second_col)
        self.table.setItem(row_index, 2, third_col)
        self.table.setItem(row_index, 3, fourth_col)
        self.table.setItem(row_index, 4, fifth_col)
        self.table.setItem(row_index, 5, sixth_col)
        self.table.setItem(row_index, 6, seventh_col)
        self.table.setItem(row_index, 7, eighth_col)
        self.table.setItem(row_index, 8, ninth_col)

        self.table.update()

    @staticmethod
    def pretty_double(value) -> str:
        return "{:.8f}".format(value)

    def update_progress_bar(self):
        current = self.progress_bar.value()
        self.progress_bar.setValue(current + self.progress_bar_step)

    @staticmethod
    def get_calculation_error(analytical: AnalyticallyCalculatedProcess,
                              numerical: NumericallyCalculatedProcess):
        errors: np.ndarray = np.absolute(numerical.get_solution() - analytical.get_solution())
        return errors.max()

    def init_report_params(self):
        self.params[7] = int(self.params[0])  # set the x_num equals to the l
        numerical = create_numerical(self.scheme_type, self.params, False)
        self.params[8] = numerical.get_min_t_num()  # set the t_num corresponding to the x_num
        self.x_scale = 4 // numerical.get_x_convergence_rate()
        self.t_scale = 4 // numerical.get_t_convergence_rate()
        self.iterations_num = int(self.iterations_num_edit.text())
        self.progress_bar_step = 100 // self.iterations_num

    def iterations_num_change_handler(self):
        if self.iterations_num_edit.hasAcceptableInput():
            self.iterations_num_edit.setStyleSheet(self.DEFAULT_STYLE)
            self.start_btn.setEnabled(True)
        else:
            self.iterations_num_edit.setStyleSheet(self.DANGER_STYLE)
            self.start_btn.setEnabled(False)

    def create_ui(self):
        self.table = QTableWidget()
        self.progress_bar = QProgressBar()
        self.iterations_num_label = QLabel()
        self.iterations_num_edit = QLineEdit()
        self.start_btn = QPushButton()
        self.close_btn = QPushButton()

    def set_defaults(self):
        self.iterations_num_edit.setText(str(3))

    def configure_ui(self):
        self.table.setColumnCount(self.columns_num)
        self.table.setHorizontalHeaderLabels([
            "N",
            "Число\nинтервалов\nпо x",
            "Число\nинтервалов\nпо t",
            "Шаг\nпо x",
            "Шаг\nпо t",
            "Погрешность\nчисленного\nрешения",
            "Отношение\nшагов\nпо x",
            "Отношение\nшагов\nпо t",
            "Отношение\nпогрешностей\nчисленного\nрешения"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table.verticalHeader().hide()
        self.table.setFixedWidth(self.get_table_width())

        self.iterations_num_label.setText("Количество итераций")
        self.start_btn.setText("Начать иследование")
        self.iterations_num_edit.setValidator(QIntValidator(1, 10))
        self.iterations_num_edit.setFixedWidth(30)
        self.iterations_num_edit.setAlignment(Qt.AlignCenter)
        self.iterations_num_edit.textChanged.connect(self.iterations_num_change_handler)
        self.start_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.start_btn.clicked.connect(self.start_convergence_report)

        self.progress_bar.setMaximum(100)

        self.close_btn.setText("Закрыть")
        self.close_btn.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.addWidget(self.table)

        init_box = QHBoxLayout()
        init_box.setAlignment(Qt.AlignCenter)
        init_box.addWidget(self.iterations_num_label)
        init_box.addWidget(self.iterations_num_edit)
        init_box.addWidget(self.start_btn)
        layout.addLayout(init_box)

        layout.addWidget(self.progress_bar)
        layout.addWidget(self.close_btn)
        self.setLayout(layout)
        self.setWindowTitle("Экспериментальное исследование сходимости")
        self.setFixedHeight(self.sizeHint().height())
        self.setFixedWidth(self.sizeHint().width())
        self.center()

    def get_table_width(self):
        width = 4
        for i in range(self.columns_num):
            width += self.table.columnWidth(i)
        return width

    def set_close_handler(self, close_handler: Callable):
        self.close_handler = close_handler

    def closeEvent(self, event):
        event.accept()
        if self.close_handler is not None:
            self.close_handler()

    def center(self):
        qt_rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

    class FooterLayout(Enum):
        INIT = 0
        PROGRESS = 1
        FINAL = 2

    def set_layout(self, layout_type: FooterLayout):
        if layout_type == self.FooterLayout.INIT:
            self.iterations_num_label.show()
            self.iterations_num_edit.show()
            self.start_btn.show()
            self.progress_bar.hide()
            self.close_btn.hide()
        elif layout_type == self.FooterLayout.PROGRESS:
            self.iterations_num_label.hide()
            self.iterations_num_edit.hide()
            self.start_btn.hide()
            self.progress_bar.show()
            self.close_btn.hide()
        elif layout_type == self.FooterLayout.FINAL:
            self.iterations_num_label.hide()
            self.iterations_num_edit.hide()
            self.start_btn.hide()
            self.progress_bar.hide()
            self.close_btn.show()
