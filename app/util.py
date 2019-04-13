from enum import Enum
from typing import Callable, List


from app.process.numerically_calculated_process import NumericallyCalculatedProcess
from app.process.explicitly_calculated_process import ExplicitlyCalculatedProcess
from app.process.inexplicitly_calculated_process import InexplicitlyCalculatedProcess
from app.process.analytically_calculated_process import AnalyticallyCalculatedProcess


class SchemeType(Enum):
    EXPLICIT = 1
    INEXPLICIT = 2


def create_analytical(params: List[float or int],
                      calculate_immediately: bool = True):
    (l, t, s, a, k, c, u0, x_num, t_num, eps) = params
    phi: Callable = lambda x: 0
    xi: Callable = lambda x: -4 * x ** 2 / l ** 2 + 4 * x / l + u0
    return AnalyticallyCalculatedProcess(l, t, s, a, k, c, u0, phi, xi, x_num, t_num, eps, calculate_immediately)


def create_explicit(params: List[float or int],
                    calculate_immediately: bool = True) -> ExplicitlyCalculatedProcess:
    (l, t, s, a, k, c, u0, x_num, t_num, eps) = params
    phi: Callable = lambda x: 0
    xi: Callable = lambda x: -4 * x ** 2 / l ** 2 + 4 * x / l + u0
    return ExplicitlyCalculatedProcess(l, t, s, a, k, c, u0, phi, xi, x_num, t_num, calculate_immediately)


def create_inexplicit(params: List[float or int],
                      calculate_immediately: bool = True) -> InexplicitlyCalculatedProcess:
    (l, t, s, a, k, c, u0, x_num, t_num, eps) = params
    phi: Callable = lambda x: 0
    xi: Callable = lambda x: -4 * x ** 2 / l ** 2 + 4 * x / l + u0
    return InexplicitlyCalculatedProcess(l, t, s, a, k, c, u0, phi, xi, x_num, t_num, calculate_immediately)


def create_numerical(scheme_type: SchemeType,
                     params: List[float or int],
                     calculate_immediately: bool = True) -> NumericallyCalculatedProcess:
    if scheme_type == SchemeType.EXPLICIT:
        return create_explicit(params, calculate_immediately)
    elif scheme_type == SchemeType.INEXPLICIT:
        return create_inexplicit(params, calculate_immediately)
