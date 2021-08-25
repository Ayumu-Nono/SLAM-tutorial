from typing import List
import copy

import numpy as np

from ._status import Status
from ._util import resampling
from ._parameter import seed, n_particle

np.random.seed(seed=seed)


class Optimizer:
    """particle filterの亜種"""
    def __init__(
        self, init_status: Status,
        n_particle=n_particle, init_noise_rate=0.3
    ) -> None:
        """
            args:
                n_particle: 粒子数
                score_ave_thre: 平均スコアの閾値. 終了条件に使う
                init_status: 初期分布を生成するのに用いる
        """
        init_status = copy.deepcopy(init_status)
        self.n_particle: int = n_particle
        self.score: float = 0.0
        self.particles: List[Status] = [
            Status(
                position=tuple(
                    init_status.position + np.random.randn(2) * init_noise_rate
                ),
                angle=init_status.angle + np.random.randn() * init_noise_rate
            ) for i in range(n_particle)
        ]
        self.score_func = None
        self.opzd_status: Status = None
    
    def set_score_function(self, func) -> None:
        self.score_func = func
    
    def _calc_weighted_status(self, weights: np.ndarray) -> Status:
        positions: np.ndarray = np.array([p.position for p in self.particles])
        angles: np.ndarray = np.array([p.angle for p in self.particles])
        assert len(weights) == len(positions)
        status: Status = Status(
            position=np.average(positions, weights=weights, axis=0),
            angle=np.average(angles, weights=weights)
        )
        return status
    
    def _scatter_particles(self, noise_rate=0.01) -> None:
        for p in self.particles:
            p.change(
                position=p.position + np.random.randn(2) * noise_rate,
                angle=p.angle + np.random.randn() * noise_rate
            )
    
    def optimize(self, score_thre=0.4, max_count=2) -> None:
        count: int = 0
        while (self.score < score_thre and count < max_count):
            assert self.score_func is not None, "先にscore_funcをsetしてください"
            self._scatter_particles()
            scores: np.ndarray = np.array([
                self.score_func(status=status) for status in self.particles
            ])
            weights: np.ndarray = scores / np.sum(scores)
            assert np.abs(np.sum(weights) - 1.0) < 0.001, np.sum(weights)
            # リサンプリング
            k = resampling(weights=weights, n_particle=self.n_particle)
            self.particles = [copy.deepcopy(self.particles[i]) for i in k]
            self.opzd_status = self._calc_weighted_status(weights=weights)
            # 後処理
            scores = np.array([
                self.score_func(status=status) for status in self.particles
            ])
            weights = scores / np.sum(scores)
            assert np.abs(np.sum(weights) - 1.0) < 0.001, np.sum(weights)
            self.score = np.average(scores, weights=weights)
            if count % 1 == 0:
                print(count, self.score)
            count += 1
        
    def close(self) -> None:
        del self
    



