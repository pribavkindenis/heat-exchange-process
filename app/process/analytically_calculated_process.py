from app.process.process import Process
from typing import *
import multiprocessing as mp
import numpy as np


def parallel_batch(i, x, k, c, l, mu, t):
    nu = np.pi ** 2 * i ** 2
    return (np.exp((-k * nu / (c * l ** 2) + mu) * t)
            * (-8 / nu * (np.cos(np.pi * i) + 1))
            * np.cos(np.pi * i / l * x))

class AnalyticallyCalculatedProcess(Process):
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
                 eps: int,
                 calculate_immediately: bool = True):
        self._eps = eps
        self._pool = mp.Pool(processes=mp.cpu_count())
        super().__init__(l, t, s, a, k, c, u0, phi, xi, x_num, t_num, calculate_immediately)

    def _calculate_process(self) -> np.ndarray:
        mu = -4 * self._a / (self._c * np.sqrt(self._s))
        x, t = np.meshgrid(self._xn, self._tn)
        u = self._calculate_u(x, t, mu)
        return np.array(u)

    def _calculate_u(self, x, t, mu):
        res = 2 / 3 * np.exp(mu * t)
        map_arguments = ((i, x, self._k, self._c, self._l, mu, t) for i in range(1, self._calculate_n()))
        map_results = self._pool.starmap(parallel_batch, map_arguments)
        for map_res in map_results:
            res += map_res
        return res + self._u0

    def _calculate_n(self) -> int:
        return int(np.ceil(16 / (self._eps*np.pi**2) - 1))

    def get_solution_on(self, index) -> np.ndarray:
        return self._u[index]
