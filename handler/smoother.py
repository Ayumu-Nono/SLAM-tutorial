import numpy as np

from db.controller.status_controller import StatusController
from db.controller.scan_controller import ScanController


class Smoother:
    def __init__(
        self,
        pred_status_controller: StatusController,
        smtd_status_controller: StatusController,
        scan_controller: ScanController
    ) -> None:
        assert isinstance(pred_status_controller, StatusController)
        assert isinstance(smtd_status_controller, StatusController)
        assert isinstance(scan_controller, ScanController)
        self.__pred_status_controller: StatusController = pred_status_controller
        self.__smtd_status_controller: StatusController = smtd_status_controller
        self.__scan_statas_controller: ScanController = scan_controller

    def set_initial_status(self, position: np.ndarray, angle: float) -> bool:
        assert self.__smtd_status_controller.get_latest_tstep_as_int() == 0
        is_success = self.__smtd_status_controller.push_with_arr(position, angle)
        return is_success

    