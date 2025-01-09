def add(x: int, y: int) -> int:
    return x + y

def subtract(x: int, y: int) -> int:
    return x - y

def increment(x: int) -> int:
    """Increment an integer by one."""
    return x + 1

def test_add():
    assert add(1, 2) == 3

def test_subtract():
    assert subtract(1, 2) == -1

def test_increment():
    assert increment(1) == 2