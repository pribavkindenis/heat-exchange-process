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

    @abstractmethod
    def get_solution(self, index) -> np.ndarray:
        pass

    @abstractmethod
    def get_x(self) -> np.ndarray:
        pass

    @abstractmethod
    def get_t(self) -> np.ndarray:
        pass

    @abstractmethod
    def get_ht(self) -> float:
        pass
