import math

import scipy

# from Charts import *


# from scipy.stats import t

# CONST
pi = 3.14159265
Yc = 17.3 * (10 ** -6)


class Calculation:
    def __init__(self, M_x, B_x, alpha, beta, E):
        self.P_in: float = self.F((beta - M_x) / B_x) - self.F((alpha - M_x) / B_x)
        self.P_out: float = 2 * self.F(E / B_x)

    def F(self, x: float) -> float:
        return scipy.stats.norm.cdf(x) - 0.5


if __name__ == "__main__":
    M_x = 7.4
    B_x = 0.8
    alpha = 7
    beta = 8.2
    E = 0.2
    calculation = Calculation(M_x, B_x, alpha, beta, E)
    print(calculation.P_in, calculation.P_out)
    # ChartLinePLT(calculation.chart_v_y_data)
    # plt.legend()
    # plt.show()
