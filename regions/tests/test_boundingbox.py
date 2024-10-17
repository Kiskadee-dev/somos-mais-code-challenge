from regions.boundingbox import BoundingBox


def test_boundingbox_size():
    b = BoundingBox(0, 0, 10, 10)
    assert b.size() == 10**2

    b = BoundingBox(10, 10, 10, 10)
    assert b.size() == 0

    b = BoundingBox(-10, -10, 0, 0)
    assert b.size() == 10**2


def test_boundingbox_has():
    b = BoundingBox(0, 0, 10, 10)
    assert b.has(5, 5) is True
    assert b.has(0.01, 9.9) is True
    assert b.has(0, 0) is False
    assert b.has(10, 10) is False

    b = BoundingBox(-10, -10, 0, 0)
    assert b.has(-5, -5) is True
    assert b.has(-0.01, -9.9) is True
    assert b.has(0, 0) is False
    assert b.has(10, 10) is False
