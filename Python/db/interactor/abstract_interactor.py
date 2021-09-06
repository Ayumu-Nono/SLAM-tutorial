from abc import ABCMeta, abstractmethod
#ABCモジュールで抽象クラスを作る
#親abcメタ　子　command status　 @abstractmethodの内容を必ずoverrideさせる。

class AbstractInteractor(metaclass=ABCMeta):
    @abstractmethod
    def push(self, val):
        pass

    @abstractmethod
    def get_latest(self):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_len(self):
        pass
