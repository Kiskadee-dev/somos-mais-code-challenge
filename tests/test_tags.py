from tags import BoundingBox


def test_boundingbox_size():
    b = BoundingBox(0, 0, 10, 10)
    assert b.size() == 10**2

    b = BoundingBox(10, 10, 10, 10)
    assert b.size() == 0, "Points on top of each other should reduce the area"
