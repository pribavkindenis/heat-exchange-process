from abc import ABC, abstractmethod
from typing import *
import numpy as np


class Process(ABC):
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
        self._l = l
        self._t = t
        self._s = s
        self._a = a
        self._k = k
        self._c = c
        self._u0 = u0
        self._phi = phi
        self._xi = xi
        self._x_num = x_num
        self._t_num = t_num
        self._xn, self._hx = np.linspace(0, self._l, self._x_num, retstep=True)
        self._tn, self._ht = np.linspace(0, self._t, self._t_num, retstep=True)
        self._u = self._calculate_process()

    @abstractmethod
    def _calculate_process(self):
        pass

    @abstractmethod
    def get_solution(self, index) -> np.ndarray:
        pass

    def get_xn(self) -> np.ndarray:
        return self._xn

    def get_tn(self) -> np.ndarray:
        return self._tn

    def get_hx(self) -> float:
        return self._hx

    def get_ht(self) -> float:
        return self._ht
