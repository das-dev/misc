from math import hypot
from array import array


class Vector:
    """
    >>> v = Vector(3, 4)
    >>> v.x, v.y
    (3.0, 4.0)
    >>> v
    Vector2D(3, 4)
    >>> v_clone = eval(repr(v))
    >>> v_clone
    Vector2D(3, 4)
    >>> v == v_clone
    True
    >>> print(v)
    (3.0, 4.0)
    >>> octets = bytes(v)
    >>> octets
    b'd\\x00\\x00\\x00\\x00\\x00\\x00\\x08@\\x00\\x00\\x00\\x00\\x00\\x00\\x10@'
    >>> Vector.frombytes(octets)
    Vector2D(3, 4)
    >>> abs(v)
    5.0
    >>> bool(v), bool(Vector(0, 0))
    (True, False)
    """

    typecode = 'd'

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        return f'{type(self).__name__}({self.x:.0f}, {self.y:.0f})'

    def __str__(self):
        return str(tuple(self))

    def __abs__(self):
        return hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))

    def __iter__(self):
        return iter((self.x, self.y))

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __bytes__(self):
        return (bytes([ord(self.typecode)])) + (bytes(array(self.typecode, self)))

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(*memv)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
