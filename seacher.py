from typing import List

import utils
import backend
import instance


def _filter_no_items(inst: instance.Instance, points: List[utils.Point]):
    return list(filter(lambda p: len(inst.located[p[0]][p[1]]) != 0, points))


def search(inst: instance.Instance, back: backend.IBackend, point: utils.Point):
    points_around = utils.points_around(point, inst.radius, inst.x_size, inst.y_size)

    # remove all that don't have any items
    points_around = _filter_no_items(inst, points_around)
    closest = utils.closest_point(points_around, point)

    # nothing around us has any trash so lets return
    if closest is None:
        return

    point_within_radius = utils.points_around(closest, inst.radius, inst.x_size, inst.y_size)
    point_within_radius = _filter_no_items(inst, point_within_radius)
    next_point = closest
    current_point = closest
    while next_point is not None:
        point_within_radius = list(filter(lambda p: p != next_point, point_within_radius))

        if current_point != next_point:
            utils.move_bot(back, current_point, next_point)
        current_point = next_point
        next_point = utils.closest_point(point_within_radius, current_point)

        # Make a shallow copy of the list because collect will delete from located
        x, y = current_point[1]
        for item_id in list(inst.located[x][y]):
            inst.collect(back, item_id, x, y)

    # move back to the anchor position
    utils.move_bot(back, point, closest)
    inst.scan(back)

    search(inst, back, closest)
