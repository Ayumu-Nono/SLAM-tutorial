import numpy as np

from db.controller.status_controller import StatusController


if __name__ == "__main__":
    status_controller = StatusController()
    posiion = np.array([1., 2.])
    angle = 0.5
    is_success = status_controller.push_with_arr(position=posiion, angle=angle)
    print(status_controller.get_latest_position_as_arr())
    