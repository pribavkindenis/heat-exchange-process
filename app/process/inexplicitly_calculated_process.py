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
        self._xn, self._hx = np.linspace(0, self._l, self._x_num, retstep=True)
        self._tn, self._ht = np.linspace(0, self._t, self._t_num, retstep=True)
        self._u = self._calculate_process()

    def _calculate_process(self) -> np.ndarray:
        # TODO implement calculation of an inexplicit scheme here. Result must be a two dimensional array
        return self._xn

    def get_solution(self, index) -> np.ndarray:
        # TODO change this method to return self._u[index]
        return self._xn

    def get_xn(self) -> np.ndarray:
        return self._xn

    def get_tn(self) -> np.ndarray:
        return self._tn

    def get_ht(self) -> float:
        return self._ht

    def get_max_x_num(self) -> int:
        # TODO
        return 0

    def get_min_t_num(self) -> int:
        # TODO
        return 0

