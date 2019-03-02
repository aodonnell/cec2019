import logging
import math
from typing import Tuple, List, Optional

import instance
from backend import IBackend

FORMAT = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

Point = Tuple[int, int]
Points = List[Point]


def get_logger(name: str, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    handler = logging.StreamHandler()
    handler.setFormatter(FORMAT)
    logger.addHandler(handler)

    return logger


def transform_path(inst: instance.Instance, starting_point: Tuple[int, int], path: list):
    if starting_point[0] == inst.x_min and starting_point[1] == inst.x_min:
        transformed_path = path
    elif starting_point[0] == inst.x_max and starting_point[1] == inst.y_max:
        transformed_path = path[::-1]
    elif starting_point[0] == inst.x_max and starting_point[1] == inst.y_min:
        transformed_path = [(x, -y) for (x, y) in path]
    else:
        transformed_path = [(-x, y) for (x, y) in path]

    translated_path = [(x + inst.x_min, y + inst.y_min) for (x, y) in transformed_path]

    return translated_path


def clamp(value: int, maximum: int):
    return max(0, min(maximum, value))


def points_around(point: Tuple[int, int], radius: int, x_max: int, y_max: int):
    around: List[Point] = []
    for y in range(-radius, radius + 1):
        for x in range(-radius + abs(y), radius - abs(y) + 1):
            around.append((clamp(point[0] + x, x_max), clamp(point[1] + y, y_max)))
    return around


def manhattan_distance(p1: Point, p2: Point):
    return abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])


def closest_point(points: List[Point], target: Point) -> Optional[Point]:
    closest: Tuple[int, Point] = None

    for around in points:
        distance = manhattan_distance(around, target)
        if closest and distance >= closest[0]:
            continue

        closest = (distance, around)

    if closest is None:
        return None

    return closest[1]


def find_waste_index(items: List[dict], waste_type: str):
    for i in range(0, len(items)):
        if items[i]['type'] == waste_type:
            return i

    return -1


def dump(inst: instance.Instance):
    """
    dump waste in the appropriate bin

    :param bkend: instance of the backend
    :param inst: instance of the current state
    :param current_location: tuple with coordinates for current location
    :return: None
    """
    organic_bin_loc = inst.bin_location_organic
    recycle_bin_loc = inst.bin_location_recycle
    garbage_bin_loc = inst.bin_location_garbage

    organic_bin_cap = inst.capacity_organic
    recycle_bin_cap = inst.capacity_recycle
    garbage_bin_cap = inst.capacity_garbage

    items_held = inst.items_held

    while items_held:
        dumped_organic = 0
        dumped_recycle = 0
        dumped_garbage = 0

        inst.move_to_point(organic_bin_loc)
        while dumped_organic <= organic_bin_cap:
            waste_index = find_waste_index(items_held, 'ORGANIC')

            if waste_index == -1:
                break

            inst.unload(waste_index)
            dumped_organic += 1

        inst.move_to_point(recycle_bin_loc)
        while dumped_recycle <= recycle_bin_cap:
            waste_index = find_waste_index(items_held, 'RECYCLE')

            if waste_index == -1:
                break

            inst.unload(waste_index)
            dumped_recycle += 1

        inst.move_to_point(garbage_bin_loc)
        while dumped_garbage <= garbage_bin_cap:
            waste_index = find_waste_index(items_held, 'GARBAGE')

            if waste_index == -1:
                break

            inst.unload(waste_index)
            dumped_garbage += 1


def clip_coord(x, y, max_x, max_y):
    """
    Clip coordinate between 0 and a set maximum. return a tuple containing the coord

    :param x:
    :param y:
    :param max_x:
    :param max_y:
    :return:
    """

    x = max(0, min(x, max_x - 1))
    y = max(0, min(y, max_y - 1))
    return x, y


def get_scan_path(size_x: int, size_y: int, scan_w):
    """
    Get ideal scan path coordinates

    :param size_x:
    :param size_y:
    :param scan_w:
    :return:
    """
    path = []

    curr_x = 0
    curr_y = 0

    # always start at top
    path.append((curr_x, curr_y))

    half_w = math.ceil(scan_w / 2)

    stride_x = scan_w + 1

    stride_y = -scan_w

    # from top left until we are completely out of bounds 
    # (last scan would ideally be the bottom right corner)
    while True:

        # if we're out of bounds already, go down our scan width +1 and our scan width over to the right.
        if curr_x >= size_x or curr_x < 0 or curr_y >= size_y or curr_y < 0:

            if curr_x >= (size_x - scan_w) and (curr_y >= size_y - scan_w):
                break

            curr_y += scan_w + 1
            curr_x += scan_w

            # add the start of the next spiral to our path
            path.append(clip_coord(curr_x, curr_y, size_x, size_y))

            # reverse x and y direction.
            stride_x *= -1
            stride_y *= -1

        # stride no matter what
        curr_x += stride_x
        curr_y += stride_y

        path.append(clip_coord(curr_x, curr_y, size_x, size_y))

    return path
