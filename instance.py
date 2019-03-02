import dataclasses


@dataclasses.dataclass
class Instance:
    x_min: int
    x_max: int
    y_min: int
    y_max: int

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
