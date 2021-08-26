from abc import ABCMeta, abstractmethod


class AbstractInteractor(metaclass=ABCMeta):
    @abstractmethod
    def push(self, val):
        pass

    @abstractmethod
    def get_latest(self):
        pass
