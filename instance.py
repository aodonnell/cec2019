from typing import List, Dict

import backend
import dataclasses

import utils


@dataclasses.dataclass
class Instance:
    x_min: int
    x_max: int
    y_min: int
    y_max: int
    radius: int
    time_turn: int
    time_move: int
    time_scan: int
    time_collect: int
    time_unload: int
    bin_collection_cycle: int
    capacity_organic: int
    capacity_recycle: int
    capacity_garbage: int
    total_organic: int
    total_recycle: int
    total_garbage: int
    bin_location_organic: utils.Point
    bin_location_recycle: utils.Point
    bin_location_garbage: utils.Point
    items_held: List[dict] = []
    time_spent: int = 0
    located: List[List[Dict[int, dict]]] = dataclasses.field(init=False, default_factory=list)

    @property
    def x_size(self):
        return self.x_max - self.x_min

    @property
    def y_size(self):
        return self.y_max - self.y_min

    def __post_init__(self):
        # Init the grid to x_size by y_size
        self.located = [[dict() for _ in range(self.y_size)] for _ in range(self.x_size)]

    def scan(self, back: backend.Backend):
        payload = back.scan()

        for item in payload['itemsLocated']:
            self.located[item['x']][item['y']][item['id']] = item

    @classmethod
    def from_payload(cls, payload: dict):
        constants = payload['constants']
        dimensions = constants['ROOM_DIMENSIONS']
        time = constants['TIME']
        capacities = constants['BIN_CAPACITY']
        totals = constants['TOTAL_COUNT']
        locations = constants['BIN_LOCATION']
        return cls(
            dimensions['X_MIN'],
            dimensions['X_MAX'],
            dimensions['Y_MIN'],
            dimensions['Y_MAX'],
            constants['SCAN_RADIUS'],
            time['TURN'],
            time['MOVE'],
            time['SCAN_AREA'],
            time['COLLECT_ITEM'],
            time['UNLOAD_TIME'],
            constants['BIN_COLLECTION_CYCLE'],
            capacities['ORGANIC'],
            capacities['RECYCLE'],
            capacities['GARBAGE'],
            totals['ORGANIC'],
            totals['RECYCLE'],
            totals['GARBAGE'],
            (locations['ORGANIC']['X'], locations['ORGANIC']['Y']),
            (locations['RECYCLE']['X'], locations['RECYCLE']['Y']),
            (locations['GARBAGE']['X'], locations['GARBAGE']['Y'])
        )
