import logging

import dataclasses

FORMAT = logging.Formatter('%(name)s - %(levelname)s - %(message)s')


def get_logger(name: str, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    handler = logging.StreamHandler()
    handler.setFormatter(FORMAT)
    logger.addHandler(handler)

    return logger


@dataclasses.dataclass
class Point:
    x: int
    y: int
