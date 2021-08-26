from db.controller.status_controller import StatusController
from db.controller.scan_controller import ScanController


class Optimizer:
    def __init__(
        self,
        status_controller: StatusController,
        scan_controller: ScanController
    ) -> None:
        assert isinstance(status_controller, StatusController)
        assert isinstance(scan_controller, ScanController)
        self.status_controller: StatusController = status_controller
        self.scan_controller: ScanController = scan_controller
        
        