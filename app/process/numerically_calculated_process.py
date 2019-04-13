from app.process.process import Process
from abc import ABC, abstractmethod
from typing import *


class NumericallyCalculatedProcess(Process, ABC):
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
                 t_num: int,
                 calculate_immediately: bool = True):
        super().__init__(l, t, s, a, k, c, u0, phi, xi, x_num, t_num, calculate_immediately)

    @abstractmethod
    def get_max_x_num(self) -> int:
        pass

    @abstractmethod
    def get_min_t_num(self) -> int:
        pass

    @abstractmethod
    def get_x_convergence_rate(self) -> int:
        pass

    @abstractmethod
    def get_t_convergence_rate(self) -> int:
        pass
