from model.command import Command
from db.repository.command_db import CommandDB
from .abstract_interactor import AbstractInteractor


class CommandInteractor(AbstractInteractor):
    def __init__(self) -> None:
        self.__decision_db: CommandDB = CommandDB()

    def push(self, decision: Command) -> bool:
        assert isinstance(decision, Command)
        is_success: bool = self.__decision_db.push(decision)
        return is_success

    def get_latest(self) -> Command:
        assert self.__decision_db.exist()
        return self.__decision_db.get(index=-1)

    def get_all(self) -> None:
        raise FutureWarning("Don't use this function.")
