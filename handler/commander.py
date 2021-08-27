import numpy as np

from db.controller.command_controller import CommandController


class Commander:
    def __init__(
        self,
        command_controller: CommandController
    ) -> None:
        self.__command_controller: CommandController = command_controller

    def command(self) -> bool:
        is_success = self.__command_controller.push_with_float(
            10.0, 5.0
        )
        return is_success

        