from typing import List, Optional
import itertools
import copy

import numpy as np

from ._status import Status
from ._senser import IdealSenser, ScanData
from ._pilot import Pilot, Decision
from ._estimater import Estimater
from ._storage import Storage
from .world import World


dt = 0.01
seed = 10
np.random.seed(seed=seed)


class IdealRobot:
    """
        position: (x, y)
        velocity: float
        angle: radian -pi~pi
    """
    def __init__(self, position: tuple, angle: float) -> None:
        self.status: Status = Status(position=position, angle=angle)
        self.estd_status: Status = Status(position=position, angle=angle)
        self.senser: IdealSenser = IdealSenser()
        self.pilot: Pilot = Pilot()
        self.estimater: Estimater = Estimater()
        self.storage: Storage = Storage()

    def move(
        self, velocity: float, angular_velocity: float, dt: float,
        noise_rate=1  # ノイズ付加の割合
    ) -> None:
        old_position: np.ndarray = np.array(self.status.position)
        old_angle: float = self.status.angle
        dx = velocity * np.cos(self.status.angle) * dt
        dy = velocity * np.sin(self.status.angle) * dt
        d_position: np.ndarray = np.array([dx, dy])
        d_theta: float = angular_velocity * dt
        new_position: np.ndarray = old_position + d_position
        new_angle: float = old_angle + d_theta
        # noise
        new_position += np.random.randn() * noise_rate * 0.3 * d_position
        new_angle += np.random.randn() * noise_rate * 1.5 * d_theta
        self.status.change(position=tuple(new_position), angle=new_angle)

    def see(self, world: World) -> ScanData:
        _segments = [obs.segments for obs in world.obstacles]
        segments: list = list(itertools.chain.from_iterable(_segments))
        scan_data: ScanData = self.senser.scan(
            self_position=self.status.position,
            self_angle=self.status.angle,
            segments=segments
        )
        return scan_data

    def orient(
        self,
        ref_status: Status, ref_scan: Optional[ScanData],
        now_scan: Optional[ScanData], now_decision: Optional[Decision]
    ) -> None:
        """orient: 自分自身を正しい位置に置く"""
        if ref_scan is not None and now_scan is not None:
            self.estd_status = self.estimater.smooth_w_scan(
                ref_status=ref_status, ref_scan=ref_scan, now_scan=now_scan
            )
        if now_decision is not None:
            self.estd_status = self.estimater.predict_w_odometory(
                old_status=ref_status, now_decision=now_decision, dt=dt
            )

    def make_decision(self, t: int, world: World) -> Decision:
        """
            return: (velocity, angular_velocity)
        """
        scan_data: ScanData = self.see(world=world)
        if t > 0:
            ref_status: Status = self.storage.robot_estd_status_list[-1]
            ref_scan_data: ScanData = self.storage.scan_data_list[-1]
            self.orient(
                ref_status=ref_status, ref_scan=ref_scan_data,
                now_scan=scan_data, now_decision=None
            )
            decision: Decision = self.pilot.decide(
                t=t,
                status=self.estd_status,
                scan_data=scan_data
            )
        else:
            decision = Decision(t=t, velocity=0, angular_velocity=0)  # 最初は動かない
        return decision

    def each_step(self, t: int, world: World) -> None:
        scan_data: ScanData = self.see(world=world)
        decision: Decision = self.make_decision(t=t, world=world)
        self.move(
            velocity=decision.velocity,
            angular_velocity=decision.angular_velocity,
            dt=dt
        )
        # 移動後の位置の予測
        self.orient(
            ref_status=self.estd_status, ref_scan=None,
            now_scan=None, now_decision=decision
        )
        # 後処理
        storage_status: dict = self.storage.store(
            robot_true_status=self.status,
            robot_estd_status=self.estd_status,
            scan_data=scan_data,
            decision=decision
        )

