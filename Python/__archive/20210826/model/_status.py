from typing import Optional


class Status:
    def __init__(self, position: tuple, angle: float) -> None:
        self.position: tuple = position
        self.angle: float = angle

    def change(self, position: Optional[tuple], angle: Optional[float]) -> None:
        if position is not None:
            self.position = position
        if angle is not None:
            self.angle = angle

