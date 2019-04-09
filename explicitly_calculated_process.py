from process import Process
import numpy as np
from typing import *


class ExplicitlyCalculatedProcess(Process):
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
        self._x, self._hx = np.linspace(0, self._l, self._x_num, retstep=True)
        self._t, self._ht = np.linspace(0, self._t, self._t_num, retstep=True)
        self._u = self._calculate_process()

    def _calculate_process(self) -> np.ndarray:
        u = [[]]

        for x in self._x:
            u[0].append(self._xi(x))

        mu = self._ht * self._k / (self._c * self._hx ** 2)
        th = self._ht * self._a / (self._c * np.sqrt(self._s))
        nu = 4*th*self._u0

        for k in range(1, self._t_num + 1):
            u.append([])
            u[k].append(self._calculate_first(u, mu, th, nu, k))

            for i in range(1, self._x_num - 1):
                u[k].append(self._calculate_middle(u, mu, th, nu, k, i))

            u[k].append(self._calculate_last(u, mu, th, nu, k))

        return np.array(u)

    def _calculate_first(self, u, mu, th, nu, k) -> float:
        return (1 - 2*mu - 4*th)*u[k-1][0] + 2*mu*u[k-1][1] + nu + self._ht*self._phi(self._x[0])

    def _calculate_middle(self, u, mu, th, nu, k, i) -> float:
        return (1 - 2*mu - 4*th)*u[k-1][i] + mu*u[k-1][i+1] + mu*u[k-1][i-1] + nu + self._ht*self._phi(self._x[i])

    def _calculate_last(self, u, mu, th, nu, k) -> float:
        return (1 - 2*mu - 4*th)*u[k-1][self._x_num-1] + 2*mu*u[k-1][self._x_num-2] \
               + nu + self._ht*self._phi(self._x[self._x_num-1])

    def get_solution(self, index) -> np.ndarray:
        return self._u[index]

    def get_x(self) -> np.ndarray:
        return self._x

    def get_t(self) -> np.ndarray:
        return self._t

    def get_ht(self) -> float:
        return self._ht
