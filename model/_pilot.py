from typing import List

from ._status import Status


class Decision:
    """
        velocity: 速度
        angular_velocity: 角速度
    """
    def __init__(
        self, t: int, velocity: float, angular_velocity: float
    ) -> None:
        self.t: int = t
        self.velocity: float = velocity
        self.angular_velocity: float = angular_velocity
        

class Pilot:
    def __init__(self) -> None:
        pass

    def decide(
        self, t: int, status: Status, scan_data: List[tuple]
    ) -> Decision:
        """
            args:
            return: (velocity, angular_velocity)
        """
        decision = Decision(t=t, velocity=10, angular_velocity=-0.5)
        return decision
        
