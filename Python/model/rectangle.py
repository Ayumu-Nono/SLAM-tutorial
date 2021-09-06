from typing import List


class Rectangle:
    def __init__(self, xy: tuple, width: float, height: float) -> None:
        assert isinstance(xy, tuple)
        assert isinstance(width, float), type(width)
        assert isinstance(height, float), type(height)　#諸々確認
        self.__xy: tuple = xy
        self.__width: float = width
        self.__height: float = height
        # calc edges
        x0, y0 = xy
        self.__p1: tuple = (x0, y0)　#private関数 classのなかは2つ そとは1つ
        self.__p2: tuple = (x0 + width, y0)
        self.__p3: tuple = (x0 + width, y0 + height)
        self.__p4: tuple = (x0, y0 + height)
        self.__segments: List[tuple] = [
            (self.__p1, self.__p2),
            (self.__p2, self.__p3),
            (self.__p3, self.__p4),
            (self.__p4, self.__p1),
        ]#各座標を4行2列の配列にぶちこむ

    @property　#??? プロパティ？　読み取り専用 @property　rectangle.xyでOKに（）がいらなくなる
    def xy(self) -> tuple:
        return self.__xy

    @property
    def width(self) -> float:
        return self.__width

    @property
    def height(self) -> float:
        return self.__height

    @property
    def p1(self) -> tuple:
        return self.__p1

    @property
    def p2(self) -> tuple:
        return self.__p2

    @property
    def p3(self) -> tuple:
        return self.__p3

    @property
    def p4(self) -> tuple:
        return self.__p4

    @property
    def segments(self) -> List[tuple]:
        return self.__segments
