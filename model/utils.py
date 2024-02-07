from scipy import interpolate
from scipy.special import expit
import numpy as np


def get_marketing_inflow(day_num: int) -> float:
    return randomize(max(interpolate.splev(day_num, get_marketing_inflow.tck), 0), 0.1)

x_points = [0, 10, 30, 60, 75, 90]
y_points = [10e6, 9.5e6, 3e6, 100, 0, 0]
get_marketing_inflow.tck = interpolate.splrep(x_points, y_points)

def get_apy_over_market_inflow(apy_over_market: float) -> float:
    res = 15e6 * expit((apy_over_market - 10) * 8 / 12)    
    return randomize(res, 0.3)

def get_churnrate_from_profit(apy_over_market: float) -> float:
    res = 0.7 * expit(-2 * apy_over_market)
    return min( max(res + 0.3 * (np.random.random() - 0.5), 0), 1.0)

def randomize(x: float, rand_mag: float) -> float:
    return x * (1 + rand_mag * (np.random.random() - 0.5))