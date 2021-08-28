from model.command import Command
from db.repository.command_db import CommandDB
from .abstract_interactor import AbstractInteractor


class CommandInteractor(AbstractInteractor):
    def __init__(self) -> None:
        self.__command_db: CommandDB = CommandDB()

    def push(self, command: Command) -> bool:
        assert isinstance(command, Command)
        is_success: bool = self.__command_db.push(command)
        return is_success

    def get_latest(self) -> Command:
        assert self.__command_db.exist()
        return self.__command_db.get(index=-1)

    def get_all(self) -> None:
        raise FutureWarning("Don't use this function.")

    def get_len(self) -> int:
        return self.__command_db.get_len()
