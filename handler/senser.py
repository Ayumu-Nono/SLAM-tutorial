import numpy as np

from db.controller.status_controller import StatusController
from db.controller.scan_controller import ScanController


class Senser:
    def __init__(
        self,
        status_controller: StatusController,
        scan_controller: ScanController
    ) -> None:
        self.status_controller: StatusController = status_controller
        self.scan_controller: ScanController = scan_controller

    def scan(self) -> bool:
        p: np.ndarray = self.status_controller.get_latest_position_as_arr()
        s: np.ndarray = np.zeros((100, 2))
        is_success: bool = self.scan_controller.push_with_arr(data=s)
        return is_success

        