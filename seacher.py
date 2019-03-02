from typing import Tuple

import utils
import backend
import instance


def search(inst: instance.Instance, backend: backend.IBackend, point: utils.Point):
    closest: Tuple[int, utils.Point] = None
    points_around = utils.points_around(point, inst.radius, inst.x_size, inst.y_size)

    for around in points_around:
        # check if there is anything there
        if len(inst.located[around[0]][around[1]]) == 0:
            continue

        distance = utils.manhattan_distance(around, point)
        if closest and distance >= closest[0]:
            continue

        closest = (distance, around)

    # nothing around us has any trash so lets return
    if closest is None:
        return

    # move to the closest location with trash
    utils.move_bot(backend, point, closest[1])


    backend.collect_item()


