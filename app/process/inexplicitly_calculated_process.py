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
                 t_num: int,
                 calculate_immediately: bool = True):
        super().__init__(l, t, s, a, k, c, u0, phi, xi, x_num, t_num, calculate_immediately)

    def _calculate_process(self) -> np.ndarray:
        u = [[]]

        for x in self._xn:
            u[0].append(self._xi(x))

        alpha = [0] * (self._x_num + 1)
        beta = [0] * (self._x_num + 1)

        gamma_1 = (self._k * self._ht) / (self._c * self._hx ** 2)
        gamma_2 = (4 * self._a * self._ht) / (self._c * self._s ** 0.5)

        for k in range(1, self._t_num + 1):
            u.append([0] * (self._x_num + 1))

            #alpha[0] = (1 + gamma_1 + gamma_2) * (1 - gamma_1) / gamma_1
            alpha[0] = 1.
            beta[0] = 0 #(u[k - 1][1] + gamma_2 * self._u0 + self._phi(self._xn[1])) * (2 + gamma_1 + gamma_2) / (1 + gamma_1 + gamma_2) - (u[k - 1][1] + gamma_2 * self._u0 + self._phi(self._xn[1])) / gamma_1

            for i in range(1, self._x_num + 1):
                if i == self._x_num:
                    u[k][i] = beta[i - 1] / (1 - alpha[i - 1])
                else:
                    alpha[i] = gamma_1 / (1 + 2 * gamma_1 + gamma_2 - gamma_1 * alpha[i - 1])
                    beta[i] = (u[k - 1][i] + gamma_2 * self._u0 + self._phi(self._xn[i]) + gamma_1 * beta[i - 1]) / (1 + 2 * gamma_1 + gamma_2 - gamma_1 * alpha[i - 1])
            for i in range(self._x_num - 1, -1, -1):
                u[k][i] = alpha[i] * u[k][i + 1] + beta[i]

        return np.array(u)

    def get_solution_on(self, index) -> np.ndarray:
        return self._u[index]

    def get_max_x_num(self) -> int:
        return self._l

    def get_min_t_num(self) -> int:
        return self._t

    def get_x_convergence_rate(self) -> int:
        return 1

    def get_t_convergence_rate(self) -> int:
        return 1

