import utils


def test_points_around():
    print(list(utils.points_around((2, 2), 2, 100, 100)))
    assert list(utils.points_around((2, 2), 2, 100, 100)) == [
        [(2, 0)],
        [(1, 1)], [(2, 1)], [(3, 1)],
        [(0, 2)], [(1, 2)], [(2, 2)], [(3, 2)], [(4, 2)],
        [(1, 3)], [(2, 3)], [(3, 3)],
        [(2, 4)]
    ]
