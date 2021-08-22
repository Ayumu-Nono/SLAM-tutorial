from typing import List

padding: float = 0.01
xmax: float = 10
ymax: float = 10
xlim: tuple = (0 - padding, xmax + padding)
ylim: tuple = (0 - padding, ymax + padding)


class Rectangle:
    def __init__(self, xy: tuple, width: float, height: float) -> None:
        self.xy: tuple = xy
        self.width: float = width
        self.height: float = height
        # calc edges
        x0, y0 = xy
        self.p1: tuple = (x0, y0)
        self.p2: tuple = (x0 + width, y0)
        self.p3: tuple = (x0 + width, y0 + height)
        self.p4: tuple = (x0, y0 + height)
        self.segments: List[tuple] = [
            (self.p1, self.p2), (self.p2, self.p3),
            (self.p3, self.p4), (self.p4, self.p1)
        ]

    def is_in(self, p: tuple) -> bool:
        """線上も内判定してる"""
        min_x, max_x = self.p1[0], self.p2[0]
        min_y, max_y = self.p1[1], self.p4[1]
        x, y = p
        return min_x <= x and x <= max_x and min_y <= y and y <= max_y


class World:
    """
        第一象限に限定
    """
    def __init__(self, obstacles: List[Rectangle]) -> None:
        self.xlim: tuple = xlim
        self.ylim: tuple = ylim
        self.obstacles: List[Rectangle] = obstacles
        self.start_point: tuple = (0, 0)
        self.goal_point: tuple = (xmax, ymax)
