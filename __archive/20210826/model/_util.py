from typing_extensions import Final
import numpy as np


def F_inv(w_cumsum, idx, u):
    """累積関数の逆関数"""
    if not np.any(w_cumsum < u):
        return 0
    k = np.max(idx[w_cumsum < u])
    return k + 1


def resampling(weights, n_particle):
    """計算量の少ない層化サンプリング"""
    idx = np.asanyarray(range(n_particle))
    u0 = np.random.uniform(0, 1 / n_particle)
    u = [1 / n_particle * i + u0 for i in range(n_particle)]
    w_cumsum = np.cumsum(weights)    
    k = np.asanyarray([F_inv(w_cumsum, idx, val) for val in u])
    return k
