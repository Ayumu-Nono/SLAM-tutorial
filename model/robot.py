from typing import List, Optional
import itertools

import numpy as np

from ._senser import IdealSenser, ScanData
from ._pilot import Pilot
from .world import World


dt = 0.01


class Status:
    def __init__(self, position: tuple, angle: float) -> None:
        self.position: tuple = position
        self.angle: float = angle

    def change(self, position: tuple, angle: float) -> None:
        self.position = position
        self.angle = angle


class IdealRobot:
    """
        position: (x, y)
        velocity: float
        angle: radian -pi~pi
    """
    def __init__(self, position: tuple, angle: float) -> None:
        self.status: Status = Status(position=position, angle=angle)
        self.senser: IdealSenser = IdealSenser()
        self.pilot: Pilot = Pilot()

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
            position=self.status.position, segments=segments
        )
        return scan_data

    def think(self, world: World) -> tuple:
        """
            return: (velocity, angular_velocity)
        """
        scan_data: ScanData = self.see(world=world)
        decision: tuple = self.pilot.decide(
            position=self.status.position, angle=self.status.angle,
            scan_data=scan_data
        )
        return decision

    def each_step(self, world: World) -> None:
        decision: tuple = self.think(world=world)
        self.move(velocity=decision[0], angular_velocity=decision[1], dt=dt)

