import math
import numpy as np

# All functions dealing with polynomial eqations are stored here.

def real_roots(coef):
    """ Returns only real roots computed with numpy """
    comp_roots = np.roots(coef)
    results = []
    for r in comp_roots:
        if r.imag == 0:
            results.append(r.real)
    return results


def quart_f(coef):
    """
    Returns only real roots of the equation for maximum four coefficients.
    Works much faster than numpy.roots() function as uses analytical method.
    """

    if coef[0] < 1e-10:
        return real_roots(coef)

    elif max(abs(coef[1]), abs(coef[2]), abs(coef[3]), abs(coef[4])) < 1e-10:
        return [0]

    elif float(abs(coef[0])) / max(abs(coef[1]), abs(coef[2]), abs(coef[3]), abs(coef[4])) < 1e-10:
        return real_roots(coef)

    else:
        a3 = float(coef[1]) / coef[0]  # Tada
        a2 = float(coef[2]) / coef[0]  # Tada
        a1 = float(coef[3]) / coef[0]  # Tada
        a0 = float(coef[4]) / coef[0]  # Tada

        T1 = -a3 / 4
        T2 = (a2 ** 2) - 3 * a3 * a1 + 12 * a0
        T3 = (2 * (a2 ** 3) - 9 * a3 * a2 * a1 + 27 * (a1 ** 2) + 27 * (a3 ** 2) * a0 - 72 * a2 * a0) / 2
        T4 = (-a3 ** 3 + 4 * a3 * a2 - 8 * a1) / 32
        T5 = (3 * (a3 ** 2) - 8 * a2) / 48

        if T3 ** 2 - T2 ** 3 < 0:
            return []
        else:
            R1 = math.sqrt(T3 ** 2 - T2 ** 3)

        R2 = abs(T3 + R1) ** (1.0 / 3)  # Tada
        if T3 + R1 < 0:
            R2 = -R2

        if abs(R2) > 1e-10:  # Tada: For example, [1,1,-3,-1,-1]
            R3 = (1.0 / 12) * (T2 / R2 + R2)
        else:
            return real_roots(coef)

        if T5 + R3 < 0:
            return []
        else:
            R4 = math.sqrt(T5 + R3)

        R5 = 2 * T5 - R3

        if abs(R4) < 1e-10:
            return real_roots(coef)
        else:
            R6 = T4 / R4

        answer = []

        if R5 - R6 > 0:
            answer.append(T1 - R4 - math.sqrt(R5 - R6))
            answer.append(T1 - R4 + math.sqrt(R5 - R6))
        elif R5 - R6 == 0:
            answer.append(T1 - R4)

        if R5 + R6 > 0:
            answer.append(T1 + R4 - math.sqrt(R5 + R6))
            answer.append(T1 + R4 + math.sqrt(R5 + R6))
        elif R5 + R6 == 0:
            answer.append(T1 + R4)

        return answer
