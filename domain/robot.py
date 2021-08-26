from handler.senser import Senser


class Robot:
    def __init__(
        self,
        senser: Senser
    ) -> None:
        assert isinstance(senser, Senser)
        self.senser: Senser = senser

    def scan(self) -> bool:
        is_success: bool = self.senser.scan()
        return is_success
        