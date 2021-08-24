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
        self, velocity: float, angular_velocity: float, dt: float
    ) -> None:
        old_position: np.ndarray = np.array(self.status.position)
        old_angle: float = self.status.angle
        dx = velocity * np.cos(self.status.angle) * dt
        dy = velocity * np.sin(self.status.angle) * dt
        d_position: np.ndarray = np.array([dx, dy])
        new_position: np.ndarray = old_position + d_position
        new_angle: float = old_angle + angular_velocity * dt
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
        self, ref_status: Status, ref_scan: ScanData, now_scan: ScanData
    ) -> None:
        """orient: 自分自身を正しい位置に置く"""
        estd_status: Status = self.estimater.estimate(
            ref_status=ref_status, ref_scan=ref_scan, now_scan=now_scan
        )
        self.estd_status = estd_status

    def think(self, t: int, world: World) -> Decision:
        """
            return: (velocity, angular_velocity)
        """
        scan_data: ScanData = self.see(world=world)
        if t > 0:
            ref_status: Status = self.storage.robot_estd_status_list[-1]
            ref_scan_data: ScanData = self.storage.scan_data_list[-1]
            old_decision: Decision = self.storage.decision_list[-1]
            self.estd_status = self.estimater.estimate(
                ref_status=ref_status,
                ref_scan=ref_scan_data,
                now_scan=scan_data,
                old_decision=old_decision,
                dt=dt
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
        decision: Decision = self.think(t=t, world=world)
        self.move(
            velocity=decision.velocity,
            angular_velocity=decision.angular_velocity,
            dt=dt
        )
        # 後処理
        storage_status: dict = self.storage.store(
            robot_true_status=self.status,
            robot_estd_status=self.estd_status,
            scan_data=scan_data,
            decision=decision
        )

