class Status:
    def __init__(self, position: tuple, angle: float) -> None:
        assert isinstance(position, tuple)
        assert isinstance(angle, float)
        self.__position: tuple = position
        self.__angle: float = angle

    @property
    def position(self) -> tuple:
        return self.__position

    @property
    def angle(self) -> float:
        return self.__angle
