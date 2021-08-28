import numpy as np

from model.status import Status
from db.interactor.status_interactor import StatusInteractor


class StatusController:
    def __init__(self) -> None:
        self.__status_interactor: StatusInteractor = StatusInteractor()

    def push_with_arr(self, position: np.ndarray, angle: float) -> bool:
        assert isinstance(position, np.ndarray)
        assert isinstance(angle, float)
        status: Status = Status(
            position=(position[0], position[1]), angle=angle
        )
        is_success: bool = self.__status_interactor.push(status=status)
        return is_success
    
    def get_latest_position_as_arr(self) -> np.ndarray:
        status: Status = self.__status_interactor.get_latest()
        return np.array(status.position)

    def get_latest_angle_as_float(self) -> float:
        status: Status = self.__status_interactor.get_latest()
        return status.angle

    def get_all_position_as_arr(self) -> np.ndarray:
        status_list = self.__status_interactor.get_all()
        return np.array([status.position for status in status_list])

    def get_latest_tstep_as_int(self) -> int:
        return self.__status_interactor.get_len()
