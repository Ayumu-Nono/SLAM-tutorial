from db.controller.command_controller import CommandController


class Commander:
    """司令出すひと"""
    def __init__(
        self,
        command_controller: CommandController
    ) -> None:
        self.__command_controller: CommandController = command_controller
    
    def set_initial_command(self, velocity: float, angular_velocity: float) -> int:
        assert self.__command_controller.get_latest_tstep_as_int() == 0
        t: int = self.__command_controller.push_with_float(
            velocity, angular_velocity
        )
        return t

    def command(self) -> int:
        t: int = self.__command_controller.push_with_float(
            1.0, .3
        )
        return t 
