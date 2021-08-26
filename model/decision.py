class Decision:
    def __init__(self, velocity: float, angular_velocity: float) -> None:
        assert isinstance(velocity, float)
        assert isinstance(angular_velocity, float)
        self.__velocity: float = velocity
        self.__anglular_velocity: float = angular_velocity

    @property
    def velocity(self) -> float:
        return self.__velocity
    
    @property
    def angular_velocity(self) -> float:
        return self.__anglular_velocity
