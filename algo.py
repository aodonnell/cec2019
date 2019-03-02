from typing import List

import utils
import instance

LOG = utils.get_logger(__file__)


def algo(inst: instance.Instance):
    # get all possible points
    points = inst.all_points

    for point in points:
        LOG.info(f'Moving to {point} from {inst.current_point}')
        inst.move_to_point(point)
        inst.scan()

        search(inst, point)


def _filter_no_items(inst: instance.Instance, points: List[utils.Point]):
    return list(filter(lambda p: len(inst.located[p[0]][p[1]]) != 0, points))


def search(inst: instance.Instance, point: utils.Point):
    # remove all that don't have any items
    points_with_items = _filter_no_items(inst, inst.all_points)
    closest = utils.closest_point(points_with_items, point)

    # nothing around us has any trash so lets return
    if closest is None:
        LOG.info(f'No items found around {point}')
        return

    LOG.info(f'Found {len(points_with_items)} points with items. Starting to search.')
    LOG.info(f'Using {closest} as anchor point')
    point_within_radius = utils.points_around(closest, inst.radius, inst.x_size, inst.y_size)
    point_within_radius = _filter_no_items(inst, point_within_radius)
    current_point = closest
    while current_point is not None:
        LOG.info(f'Moving to {current_point}')
        inst.move_to_point(current_point)

        # Make a shallow copy of the list because collect will delete from located
        x, y = current_point
        for item_id in list(inst.located[x][y]):
            LOG.info(f'Collecting {item_id} in ({x}, {y})')
            inst.collect(x, y, item_id)

        point_within_radius = list(filter(lambda p: p != current_point, point_within_radius))
        current_point = utils.closest_point(point_within_radius, current_point)

    # move back to the anchor position
    LOG.info(f'Moving back to {closest} and scanning')
    inst.move_to_point(closest)
    inst.scan()

    LOG.info('Scanning again.')
    search(inst, closest)


def dump(inst):
    """
    dump waste in the appropriate bin

    :param inst:
    :return:
    """
    organic_bin_loc = inst.bin_location_organic
    recycle_bin_loc = inst.bin_location_recycle
    garbage_bin_loc = inst.bin_location_garbage

    organic_bin_cap = inst.capacity_organic
    recycle_bin_cap = inst.capacity_recycle
    garbage_bin_cap = inst.capacity_garbage

    items_held = inst.items_held

    while inst.held_organic or inst.held_recycle or inst.held_garbage:
        dumped_organic = 0
        dumped_recycle = 0
        dumped_garbage = 0

        inst.move_to_point(organic_bin_loc)
        while dumped_organic <= organic_bin_cap:
            waste_index = utils.find_waste_index(items_held, 'ORGANIC')

            if waste_index == -1:
                break

            inst.unload(waste_index)
            dumped_organic += 1

        inst.move_to_point(recycle_bin_loc)
        while dumped_recycle <= recycle_bin_cap:
            waste_index = utils.find_waste_index(items_held, 'RECYCLE')

            if waste_index == -1:
                break

            inst.unload(waste_index)
            dumped_recycle += 1

        inst.move_to_point(garbage_bin_loc)
        while dumped_garbage <= garbage_bin_cap:
            waste_index = utils.find_waste_index(items_held, 'GARBAGE')

            if waste_index == -1:
                break

            inst.unload(waste_index)
            dumped_garbage += 1
