import numpy as np

from db.controller.command_controller import CommandController


class Commander:
    def __init__(
        self,
        command_controller: CommandController
    ) -> None:
        self.__command_controller: CommandController = command_controller

    def command(self, velocity: float, angular_velocity: float) -> bool:
        is_success = self.__command_controller.push_with_float(
            velocity, angular_velocity
        )
        return is_success

        