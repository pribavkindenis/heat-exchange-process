from typing import *
import numpy as np


class HeatProcess:

    def __init__(self,
                 x_batches: int = 55,
                 t_batches: int = 3000,
                 rod_length: int = 10,
                 experiment_time: int = 50,
                 k_cf: float = 0.65,
                 c_cf: float = 1.84,
                 s: float = 0.01,
                 alpha_cf: float = 0.005,
                 u0: int = 20,
                 phy: Callable = lambda x: 0,
                 xi: Callable = lambda x, l, f: -4*x**2/l**2 + 4*x/l + f):
        u = [[]]
        hx = rod_length / x_batches
        ht = experiment_time / t_batches

        x_range = np.arange(0, hx * x_batches + hx, hx)
        t_range = np.arange(0, ht * t_batches + ht, ht)

        for x in x_range:
            u[0].append(xi(x, rod_length, u0))

        a = ht * k_cf / c_cf
        b = 4 * alpha_cf / k_cf / np.sqrt(s)

        for k in range(1, t_batches + 1):
            u.append([])
            u[k].append(a*(2*(u[k-1][1] - u[k-1][0])/hx**2 + b*(u0 - u[k-1][0])) + ht*phy(x_range[0]) + u[k-1][0])

            for i in range(1, x_batches):
                u[k].append(a*((u[k-1][i+1] - 2*u[k-1][i] + u[k-1][i-1])/hx**2 + b*(u0 - u[k-1][i]))
                            + ht*phy(x_range[i]) + u[k-1][i])

            u[k].append(a*(2*(u[k-1][1] - u[k-1][x_batches])/hx**2 + b*(u0 - u[k-1][x_batches])) +
                        ht*phy(x_range[x_batches]) + u[k-1][x_batches])

        self.u = np.array(u)
        self.x_range = x_range
        self.t_batches = t_batches
        self.ht = ht
        self.u0 = u0
        self.experiment_time = experiment_time

