from typing import List
import itertools

import numpy as np

from ._senser import IdealSenser
from ._pilot import Pilot
from .world import World


dt = 0.01


class IdealRobot:
    """
        position: (x, y)
        velocity: float
        angle: radian -pi~pi
    """
    def __init__(self, position: tuple, angle: float) -> None:
        self.position: tuple = position
        self.angle: float = angle
        # 装備
        self.senser: IdealSenser = IdealSenser()
        self.pilot: Pilot = Pilot()

    def move(
        self, velocity: float, angular_velocity: float, dt: float
    ) -> None:
        old_position: np.ndarray = np.array(self.position)
        old_angle: float = self.angle
        dx = velocity * np.cos(self.angle) * dt
        dy = velocity * np.sin(self.angle) * dt
        d_position: np.ndarray = np.array([dx, dy])
        new_position: np.ndarray = old_position + d_position
        new_angle: float = old_angle + angular_velocity * dt
        self.position = tuple(new_position)
        self.angle = new_angle

    def see(self, world: World) -> List[tuple]:
        _segments = [obs.segments for obs in world.obstacles]
        segments: list = list(itertools.chain.from_iterable(_segments))
        scan_points: List[tuple] = self.senser.scan(position=self.position, segments=segments)
        return scan_points

    def think(self, world: World) -> tuple:
        """
            return: (velocity, angular_velocity)
        """
        scan_points: List[tuple] = self.see(world=world)
        decision: tuple = self.pilot.decide(
            position=self.position, angle=self.angle,
            scan_points=scan_points
        )
        return decision
    
    def each_step(self, world: World) -> None:
        decision: tuple = self.think(world=world)
        self.move(velocity=decision[0], angular_velocity=decision[1], dt=dt)


