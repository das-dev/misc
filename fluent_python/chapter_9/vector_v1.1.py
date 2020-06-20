from math import hypot, atan2
from array import array


class Vector:
    """
    >>> v = Vector(3, 4)
    >>> v.x, v.y
    (3.0, 4.0)
    >>> v
    Vector(3.0, 4.0)
    >>> v_clone = eval(repr(v))
    >>> v_clone
    Vector(3.0, 4.0)
    >>> v == v_clone
    True
    >>> print(v)
    (3.0, 4.0)
    >>> octets = bytes(v)
    >>> octets
    b'd\\x00\\x00\\x00\\x00\\x00\\x00\\x08@\\x00\\x00\\x00\\x00\\x00\\x00\\x10@'
    >>> Vector.frombytes(octets)
    Vector(3.0, 4.0)
    >>> abs(v)
    5.0
    >>> bool(v), bool(Vector(0, 0))
    (True, False)
    >>> format(v)
    '(3.0, 4.0)'
    >>> format(v, '.2f')
    '(3.00, 4.00)'
    >>> format(v, '.3e')
    '(3.000e+00, 4.000e+00)'
    >>> format(Vector(1, 1), 'p')
    '<1.4142135623730951, 0.7853981633974483>'
    >>> format(Vector(1, 1), '.3ep')
    '<1.414e+00, 7.854e-01>'
    >>> format(Vector(1, 1), '0.5fp')
    '<1.41421, 0.78540>'
    >>> v.x = 7
    Traceback (most recent call last):
    ...
    AttributeError: can't set attribute
    >>> v2, v3 = Vector(3.0, 4.0), Vector(3.1, 4.1),
    >>> hash(v), hash(v2), hash(v3)
    (7, 7, 1031)
    >>> v == v2
    True
    >>> {v, v2, v3}
    {Vector(3.1, 4.1), Vector(3.0, 4.0)}
    >>> int(v3)
    5
    >>> float(v3)
    5.140038910358559
    >>> complex(v3)
    (3.1+4.1j)
    """

    typecode = 'd'

    def __init__(self, x, y):
        self.__x = float(x)
        self.__y = float(y)

    def __repr__(self):
        return f'{type(self).__name__}({self.x!r}, {self.y!r})'

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

    def __format__(self, format_spec):
        if format_spec.endswith('p'):
            format_spec = format_spec[:-1]
            coords = (abs(self), self.angle())
            outer_format = '<{}, {}>'
        else:
            coords = self
            outer_format = '({}, {})'
        components = (format(c, format_spec) for c in coords)
        return outer_format.format(*components)

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)

    def __int__(self):
        return int(abs(self))

    def __float__(self):
        return abs(self)

    def __complex__(self):
        return complex(self.x, self.y)

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def angle(self):
        return atan2(self.y, self.x)

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(*memv)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
