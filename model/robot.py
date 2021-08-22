from ._senser import IdealSenser


class IdealRobot:
    """
        position: (x, y)
        velocity: float
        angle: radian -pi~pi
    """
    def __init__(self, position: tuple, velocity: float, angle: float) -> None:
        self.position: tuple = position
        self.velocity: float = velocity
        self.angle: float = angle
        # 装備
        self.senser: IdealSenser = IdealSenser()

