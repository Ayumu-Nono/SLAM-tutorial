import numpy as np
from copy import deepcopy


from db.controller.status_controller import StatusController
from db.controller.scan_controller import ScanController

from .util.smoother_util import (
    calc_score, make_particles, calc_weights,
    get_resample_indexes, scatter_particles
)


class Smoother:
    def __init__(
        self,
        pred_status_controller: StatusController,
        smtd_status_controller: StatusController,
        scan_controller: ScanController
    ) -> None:
        assert isinstance(pred_status_controller, StatusController)
        assert isinstance(smtd_status_controller, StatusController)
        assert isinstance(scan_controller, ScanController)
        self.__pred_status_controller: StatusController = pred_status_controller
        self.__smtd_status_controller: StatusController = smtd_status_controller
        self.__scan_controller: ScanController = scan_controller

    def set_initial_status(self, position: np.ndarray, angle: float) -> int:
        assert self.__smtd_status_controller.get_latest_tstep_as_int() == 0
        t: int = self.__smtd_status_controller.push_with_arr(position, angle)
        return t

    def smooth(
        self, mesh_digit: int, mesh_xs: np.ndarray, mesh_ys: np.ndarray,
        passing_rate: float, max_distance: float,
        position_vs_angle_cost_ratio: float,
        mesh_vs_status_cost_ratio: float,
        n_particle: int,
        position_scatter_rate: float,
        angle_scatter_rate: float,
        thre_score: float,
        max_iterate: int
    ) -> int:
        _2ndlatest_position: np.ndarray = self.__smtd_status_controller.get_latest_position_as_arr()
        _2ndlatest_angle: float = self.__smtd_status_controller.get_latest_angle_as_float()
        pred_position: np.ndarray = self.__pred_status_controller.get_latest_position_as_arr()
        pred_angle: float = self.__pred_status_controller.get_latest_angle_as_float()
        ref_mesh: np.ndarray = self.__scan_controller.get_2ndlatest_as_mesh(
            self_position=_2ndlatest_position, self_angle=_2ndlatest_angle,
            mesh_digit=mesh_digit, mesh_xs=mesh_xs, mesh_ys=mesh_ys
        )
        # Optimize
        positions, angles = make_particles(
            init_position=pred_position, init_angle=pred_angle,
            n_particles=n_particle,
            position_scatter_rate=position_scatter_rate,
            angle_scatter_rate=angle_scatter_rate
        )
        smtd_score = 0.0
        count = 0
        while (smtd_score < thre_score and count < max_iterate):
            assert len(positions) == len(angles)
            scores = np.array([
                calc_score(
                    mesh=self.__scan_controller.get_latest_as_mesh(
                        self_position=position,
                        self_angle=angle,
                        mesh_digit=mesh_digit, mesh_xs=mesh_xs, mesh_ys=mesh_ys
                    ),
                    ref_mesh=ref_mesh,
                    pred_position=pred_position, pred_angle=pred_angle,
                    smtd_position=position, smtd_angle=angle,
                    passing_rate=passing_rate, max_distance=max_distance,
                    position_vs_angle_cost_ratio=position_vs_angle_cost_ratio,
                    mesh_vs_status_cost_ratio=mesh_vs_status_cost_ratio
                )
                for position, angle in zip(positions, angles)
            ])

            weights = calc_weights(scores=scores)
            smtd_position = np.average(positions, axis=0, weights=weights)
            smtd_angle = np.average(angles, axis=0, weights=weights)
            smtd_score = np.average(scores, axis=0, weights=weights)
            # resample
            k = get_resample_indexes(
                weights=weights, n_particle=n_particle
            )
            positions = deepcopy(positions[k])
            angles = deepcopy(angles[k])
            positions, angles = scatter_particles(
                positions=positions, angles=angles,
                n_particles=n_particle,
                position_scatter_rate=position_scatter_rate,
                angle_scatter_rate=angle_scatter_rate
            )
            print(smtd_score)
            count += 1

        t: int = self.__smtd_status_controller.push_with_arr(smtd_position, smtd_angle)
        return t
