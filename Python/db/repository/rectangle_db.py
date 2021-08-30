from typing import List
from .abstract_db import AbstractDB
from model.rectangle import Rectangle


class RectangleDB(AbstractDB):
    def __init__(self) -> None:
        self.__rectangle_list: List[Rectangle] = []

    def get(self, index: int) -> Rectangle:
        assert isinstance(index, int)
        return self.__rectangle_list[index]

    def push(self, rectangle: Rectangle) -> bool:
        assert isinstance(rectangle, Rectangle)
        old_len: int = len(self.__rectangle_list)
        self.__rectangle_list.append(rectangle)
        return len(self.__rectangle_list) > old_len

    def exist(self) -> bool:
        return len(self.__rectangle_list) != 0

    def get_len(self) -> int:
        return len(self.__rectangle_list)