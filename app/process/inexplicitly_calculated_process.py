from app.process.numerically_calculated_process import NumericallyCalculatedProcess
import numpy as np
from typing import *


class InexplicitlyCalculatedProcess(NumericallyCalculatedProcess):
    def __init__(self,
                 l: float,
                 t: float,
                 s: float,
                 a: float,
                 k: float,
                 c: float,
                 u0: float,
                 phi: Callable,
                 xi: Callable,
                 x_num: int,
                 t_num: int):
        super().__init__(l, t, s, a, k, c, u0, phi, xi, x_num, t_num)

    def _calculate_process(self) -> np.ndarray:
        # TODO implement calculation of an inexplicit scheme here. Result must be a two dimensional array
        return self._xn

    def get_solution(self, index) -> np.ndarray:
        # TODO change this method to return self._u[index]
        return self._xn

    def get_max_x_num(self) -> int:
        # TODO
        return 0

    def get_min_t_num(self) -> int:
        # TODO
        return 0

