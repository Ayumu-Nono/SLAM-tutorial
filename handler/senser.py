import numpy as np

from db.controller.status_controller import StatusController
from db.controller.scan_controller import ScanController
from db.controller.rectangle_controller import RectangleController

from .util.senser_util import receive, irradiate


class Senser:
    def __init__(
        self,
        status_controller: StatusController,
        scan_controller: ScanController,
        rectangle_controller: RectangleController
    ) -> None:
        self.__status_controller: StatusController = status_controller
        self.__scan_controller: ScanController = scan_controller
        self.__rectangle_controller: RectangleController = rectangle_controller

    def scan(self, n_laser: int) -> bool:
        self_position = self.__status_controller.get_latest_position_as_arr()
        self_angle = self.__status_controller.get_latest_angle_as_float()
        segments = self.__rectangle_controller.get_all_segments_as_arr()
        angles: np.ndarray = np.linspace(-np.pi, np.pi, n_laser)
        scan_points: np.ndarray = np.array([
            receive(
                half_line=irradiate(position=self_position, angle=angle),
                segments=segments
            )
            for angle in angles
        ])
        assert len(scan_points) == len(angles)
        distances: np.ndarray = np.linalg.norm(
            scan_points - self_position, axis=1
        )
        data: np.ndarray = np.array([
            np.array([distances[i], angle - self_angle])
            for i, angle in enumerate(angles)
        ])

        is_success: bool = self.__scan_controller.push_with_arr(data)
        return is_success

        