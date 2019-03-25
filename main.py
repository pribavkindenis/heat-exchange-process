from matplotlib import pyplot as plt
from typing import *
import numpy as np


def calculate_u(x_batches: int = 55,
                t_batches: int = 3000,
                rod_length: int = 10,
                experiment_time: int = 50,
                k_cf: float = 0.65,
                c_cf: float = 1.84,
                s: float = 0.01,
                alpha_cf: float = 0.005,
                u0: int = 20,
                phy: Callable = lambda x: 0,
                xi: Callable = lambda x, l, f: -4*x**2/l**2 + 4*x/l + f) -> np.ndarray:
    res = [[]]

    hx = rod_length / x_batches
    ht = experiment_time / t_batches

    x_range = np.arange(0, hx * x_batches + hx, hx)
    t_range = np.arange(0, ht * t_batches + ht, ht)

    for x in x_range:
        res[0].append(xi(x, rod_length, u0))

    a = ht * k_cf / c_cf
    b = 4 * alpha_cf / k_cf / np.sqrt(s)

    for k in range(1, t_batches + 1):
        res.append([])
        res[k].append(a*(2*(res[k-1][1] - res[k-1][0])/hx**2 + b*(u0 - res[k-1][0])) + ht*phy(x_range[0]) + res[k-1][0])

        for i in range(1, x_batches):
            res[k].append(a*((res[k-1][i+1] - 2*res[k-1][i] + res[k-1][i-1])/hx**2 + b*(u0 - res[k-1][i]))
                          + ht*phy(x_range[i]) + res[k-1][i])

        res[k].append(a*(2*(res[k-1][1] - res[k-1][x_batches])/hx**2 + b*(u0 - res[k-1][x_batches])) +
                      ht*phy(x_range[x_batches]) + res[k-1][x_batches])

    res = np.array(res)

    plt.plot(x_range, res[0][:])
    plt.ylim(u0-0.5, u0+1.5)
    plt.grid()
    plt.show()

    return res


if __name__ == "__main__":
    u = calculate_u()
