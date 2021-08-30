from typing import List


class Scan:
    def __init__(self, data: List[tuple]) -> None:
        assert isinstance(data, list)
        self.__data: List[tuple] = data

    @property
    def data(self) -> List[tuple]:
        return self.__data
