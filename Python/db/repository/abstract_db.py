from abc import ABCMeta, abstractmethod


class AbstractDB(metaclass=ABCMeta):
    @abstractmethod
    def get(self, index):
        pass
    
    @abstractmethod
    def push(self, val):
        pass

    @abstractmethod
    def exist(self):
        pass

    @abstractmethod
    def get_len(self):
        pass
