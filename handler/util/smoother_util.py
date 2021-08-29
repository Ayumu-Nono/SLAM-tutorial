import numpy as np


def _calc_mesh_cost(
    mesh: np.ndarray, ref_mesh: np.ndarray,
    passing_rate: float
) -> float:
    assert mesh.shape == ref_mesh.shape
    assert np.count_nonzero(mesh) == np.sum(mesh)
    num = np.sum(mesh)
    diff = mesh - ref_mesh
    not_covered_num = np.sum(diff[diff > 0])
    assert num > not_covered_num and not_covered_num > 0
    rate = not_covered_num / num
    if rate < passing_rate:
        cost = rate
    else:
        cost = (rate - passing_rate) / (1.0 - rate)
    assert 0 <= cost and cost < 1.0
    return cost


def _calc_status_cost(
    pred_position: np.ndarray, pred_angle: float,
    smtd_position: np.ndarray, smtd_angle: float,
    max_distance: float,
    position_vs_angle_cost_ratio: float
) -> float:
    d_position = pred_position - smtd_position
    d_angle = pred_angle - smtd_angle
    distance = np.linalg.norm(d_position)
    if distance < max_distance:
        position_cost = distance / max_distance
    else:
        position_cost = 1.0
    assert np.abs(d_angle) / 2 < np.pi / 2
    angle_cost = np.sin(np.abs(d_angle) / 2)
    assert 0.0 <= position_cost and position_cost < 1.0
    assert 0.0 <= angle_cost and angle_cost < 1.0
    assert position_vs_angle_cost_ratio < 1.0 \
        and 0.0 <= position_vs_angle_cost_ratio
    return position_cost * position_vs_angle_cost_ratio \
        + angle_cost * (1 - position_vs_angle_cost_ratio)


def _calc_cost(
    mesh: np.ndarray, ref_mesh: np.ndarray,
    passing_rate: float,
    pred_position: np.ndarray, pred_angle: float,
    smtd_position: np.ndarray, smtd_angle: float,
    max_distance: float,
    position_vs_angle_cost_ratio: float,
    mesh_vs_status_cost_ratio: float
) -> float:
    mesh_cost = _calc_mesh_cost(mesh, ref_mesh, passing_rate)
    status_cost = _calc_status_cost(
        pred_position, pred_angle, smtd_position, smtd_angle,
        max_distance, position_vs_angle_cost_ratio
    )
    cost = mesh_cost * mesh_vs_status_cost_ratio\
        + status_cost * (1 - mesh_vs_status_cost_ratio)
    return cost


def _change_cost2score(cost) -> float:
    return np.exp(-cost)


def calc_score(
    mesh: np.ndarray, ref_mesh: np.ndarray,
    pred_position: np.ndarray, pred_angle: float,
    smtd_position: np.ndarray, smtd_angle: float,
    passing_rate: float,
    max_distance: float,
    position_vs_angle_cost_ratio: float,
    mesh_vs_status_cost_ratio: float
) -> float:
    cost = _calc_cost(
        mesh=mesh, ref_mesh=ref_mesh,
        pred_position=pred_position, pred_angle=pred_angle,
        smtd_position=smtd_position, smtd_angle=smtd_angle,
        passing_rate=passing_rate, max_distance=max_distance,
        position_vs_angle_cost_ratio=position_vs_angle_cost_ratio,
        mesh_vs_status_cost_ratio=mesh_vs_status_cost_ratio
    )
    score = _change_cost2score(cost)
    return score
