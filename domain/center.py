from handler.senser import Senser
from handler.motor import Motor
from handler.commander import Commander
from handler.predicter import Predicter
from handler.smoother import Smoother
from params.hyper_params import dt
from params.smoother_patams import (
    mesh_digit, mesh_xs, mesh_ys,
    passing_rate,
    max_distance,
    position_vs_angle_cost_ratio,
    mesh_vs_status_cost_ratio,
    n_particle,
    position_scatter_rate,
    angle_scatter_rate,
    thre_score, max_iterate
)


class Center:
    """制御するマン"""
    def __init__(
        self,
        senser: Senser, motor: Motor, commander: Commander,
        predicter: Predicter, smoother: Smoother
    ) -> None:
        assert isinstance(senser, Senser)
        assert isinstance(motor, Motor)
        assert isinstance(commander, Commander)
        assert isinstance(predicter, Predicter)
        assert isinstance(smoother, Smoother)
        self.__senser: Senser = senser
        self.__motor: Motor = motor
        self.__commander: Commander = commander
        self.__predicter: Predicter = predicter
        self.__smoother: Smoother = smoother

    def make_command(self) -> int:
        t: int = self.__commander.command()
        return t

    def estimate_wo_scan(self) -> int:
        t: int = self.__predicter.predict(dt)
        return t
        
    def estimate_w_scan(self) -> int:
        t: int = self.__smoother.smooth(
            mesh_digit=mesh_digit, mesh_xs=mesh_xs, mesh_ys=mesh_ys,
            passing_rate=passing_rate,
            max_distance=max_distance,
            position_vs_angle_cost_ratio=position_vs_angle_cost_ratio,
            mesh_vs_status_cost_ratio=mesh_vs_status_cost_ratio,
            n_particle=n_particle,
            position_scatter_rate=position_scatter_rate,
            angle_scatter_rate=angle_scatter_rate,
            thre_score=thre_score,
            max_iterate=max_iterate
        )
        return t

