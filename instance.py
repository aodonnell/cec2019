from typing import List, Dict, Tuple

import backend
import dataclasses

import utils

LOG = utils.get_logger(__file__)


@dataclasses.dataclass
class Instance:
    back: backend.IBackend
    x_min: int
    x_max: int
    y_min: int
    y_max: int
    radius: int
    direction: str
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
    current_point: utils.Point
    time_spent = 0
    all_points: List[utils.Point] = dataclasses.field(init=False, default_factory=list)
    located: List[List[Dict[int, dict]]] = dataclasses.field(init=False, default_factory=list)
    held_organic: List[dict] = dataclasses.field(default_factory=list)
    held_recycle: List[dict] = dataclasses.field(default_factory=list)
    held_garbage: List[dict] = dataclasses.field(default_factory=list)

    @property
    def x_size(self):
        return self.x_max - self.x_min

    @property
    def y_size(self):
        return self.y_max - self.y_min

    def __post_init__(self):
        # Init the grid to x_size by y_size
        self.located = [[dict() for _ in range(self.y_size)] for _ in range(self.x_size)]
        self.all_points = [(i, j) for j in range(self.y_size) for i in range(self.x_size)]

    def scan(self):
        payload = self.back.scan()
        self.time_spent += self.time_scan

        for item in payload['itemsLocated']:
            if item['id'] in self.located[item['x']][item['y']]:
                continue

            x, y, t = item['x'], item['y'], item['type']
            LOG.info(f'Adding {t} to ({x}, {y})')
            self.located[item['x']][item['y']][item['id']] = item

    def collect(self, x: int, y: int, item_id: int):
        self.back.collect_item(item_id)
        self.time_spent += self.time_collect

        # delete from located upon completion
        item = self.located[x][y][item_id]
        del self.located[x][y][item_id]

        t = item['type']
        if t == 'ORGANIC':
            self.held_organic.append(item)
        elif t == 'RECYCLE':
            self.held_recycle.append(item)
        elif t == 'GARBAGE':
            self.held_garbage.append(item)
        else:
            raise RuntimeError(f'Unknown type: {t}')

    def _move(self):
        self.back.move()
        self.time_spent += self.time_move

    def move_to_point(self, target: Tuple[int, int]):
        if self.current_point == target:
            return

        def move_steps(num_of_steps: int):
            for _ in range(num_of_steps):
                self._move()

        x_change = target[0] - self.current_point[0]
        y_change = target[1] - self.current_point[1]

        if x_change > 0:
            self.turn('E')
        elif x_change < 0:
            self.turn('W')
        move_steps(abs(x_change))

        if y_change > 0:
            self.turn('N')
        elif y_change < 0:
            self.turn('S')
        move_steps(abs(y_change))

        self.current_point = target

    def turn(self, direction: str):
        if self.direction == direction:
            return

        self.back.turn(direction)
        self.direction = direction
        self.time_spent += self.time_turn

    def unload(self, i: int):
        item = self.items_held[i]
        self.back.unload_item(item['id'])
        self.time_spent += self.time_unload
        self.items_held.pop(i)

        t = item['type']
        if t == 'ORGANIC':
            self.held_count_organic -= 1
        elif t == 'RECYCLE':
            self.held_count_recycle -= 1
        elif t == 'RECYCLE':
            self.held_count_recycle -= 1
        else:
            raise RuntimeError(f'Unknown type: {t}')

    @classmethod
    def from_backend(cls, back: backend.IBackend):
        payload = back.create_instance()

        constants = payload['constants']
        dimensions = constants['ROOM_DIMENSIONS']
        time = constants['TIME']
        capacities = constants['BIN_CAPACITY']
        totals = constants['TOTAL_COUNT']
        locations = constants['BIN_LOCATION']
        return cls(
            back,
            dimensions['X_MIN'],
            dimensions['X_MAX'],
            dimensions['Y_MIN'],
            dimensions['Y_MAX'],
            constants['SCAN_RADIUS'],
            payload['direction'],
            time['TURN'],
            time['MOVE'],
            time['SCAN_AREA'],
            time['COLLECT_ITEM'],
            time['UNLOAD_ITEM'],
            constants['BIN_COLLECTION_CYCLE'],
            capacities['ORGANIC'],
            capacities['RECYCLE'],
            capacities['GARBAGE'],
            totals['ORGANIC'],
            totals['RECYCLE'],
            totals['GARBAGE'],
            (locations['ORGANIC']['X'], locations['ORGANIC']['Y']),
            (locations['RECYCLE']['X'], locations['RECYCLE']['Y']),
            (locations['GARBAGE']['X'], locations['GARBAGE']['Y']),
            (payload['location']['x'], payload['location']['y']),
        )
