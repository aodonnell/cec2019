from typing import List

import dataclasses


@dataclasses.dataclass
class Instance:
    x_min: int
    x_max: int
    y_min: int
    y_max: int
    located: List[List[int]] = dataclasses.field(init=False, default_factory=list)

    @property
    def x_size(self):
        return self.x_max - self.x_min

    @property
    def y_size(self):
        return self.y_max - self.y_min

    def __post_init__(self):
        # Init the grid to x_size by y_size
        self.located = [[[] for _ in range(self.y_size)] for _ in range(self.x_size)]

    @classmethod
    def from_payload(cls, payload: dict):
        constants = payload['constants']
        dimensions = constants['ROOM_DIMENSIONS']
        return cls(
            dimensions['X_MIN'],
            dimensions['X_MAX'],
            dimensions['Y_MIN'],
            dimensions['Y_MAX'],
        )
