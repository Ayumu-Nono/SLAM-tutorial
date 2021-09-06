from typing import List
from model.rectangle import Rectangle
from db.repository.rectangle_db import RectangleDB
from .abstract_interactor import AbstractInteractor


class RectangleInteractor(AbstractInteractor):
    def __init__(self) -> None:
        self.__rectangle_db: RectangleDB = RectangleDB()

    def push(self, rectangle: Rectangle) -> bool:
        assert isinstance(rectangle, Rectangle)
        is_success: bool = self.__rectangle_db.push(rectangle)
        return is_success

    def get_latest(self) -> Rectangle:
        raise FutureWarning("この関数はrectangleでは使わないで")
        assert self.__rectangle_db.exist()
        return self.__rectangle_db.get(index=-1)

    def get_all(self) -> List[Rectangle]:
        length: int = self.__rectangle_db.get_len()
        all_rectangle: List[Rectangle] = [
            self.__rectangle_db.get(index=i)
            for i in range(length)
        ]
        return all_rectangle

    def get_len(self) -> int:
        return self.__rectangle_db.get_len()　#長方形の数を数える？？