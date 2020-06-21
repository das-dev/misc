import itertools
import math
import numbers
import reprlib
import operator

from array import array
from functools import reduce


class Vector:
    """ Multidimensional vector
    >>> Vector([3.1, 4.2])
    Vector([3.1, 4.2])
    >>> v1 = Vector([3, 4, 5])
    >>> v1
    Vector([3.0, 4.0, 5.0])
    >>> v2 = Vector(range(10))
    >>> v2
    Vector([0.0, 1.0, 2.0, 3.0, 4.0, ...])
    >>> len(v1)
    3
    >>> v1[0], v1[-1]
    (3.0, 5.0)
    >>> v2[1:4]
    Vector([1.0, 2.0, 3.0])
    >>> v2[1, 2]
    Traceback (most recent call last):
    ...
    TypeError: Vector indices must be integers
    >>> v1.x, v1.y, v1.z
    (3.0, 4.0, 5.0)
    >>> v1.x = 10
    Traceback (most recent call last):
    ...
    AttributeError: readonly attribute 'x'
    >>> v1.a = 10
    Traceback (most recent call last):
    ...
    AttributeError: can't set attributes 'a' to 'z' in Vector
    >>> hash(v1), hash(v2)
    (2, 1)
    >>> {v1, v2}
    {Vector([0.0, 1.0, 2.0, 3.0, 4.0, ...]), Vector([3.0, 4.0, 5.0])}
    >>> v1 == v2
    False
    >>> v1 == Vector([3.0, 4.0, 5.0])
    True
    >>> format(v1)
    '(3.0, 4.0, 5.0)'
    >>> format(Vector([1, 1]), 'h')
    '<(1.4142135623730951, 0.7853981633974483)>'
    >>> format(Vector([1, 1, 1]), 'h')
    '<(1.7320508075688772, 0.9553166181245093, 0.7853981633974483)>'
    >>> format(Vector([2, 2, 2]), '.3eh')
    '<(3.464e+00, 9.553e-01, 7.854e-01)>'
    """

    typecode = 'd'
    shortcut_names = 'xyzt'

    def __init__(self, components):
        self._components = array(self.typecode, components)

    def __getattr__(self, name):
        cls = type(self)
        if len(name) == 1:
            pos = cls.shortcut_names.find(name)
            if 0 <= pos < len(self):
                return self._components[pos]
        raise AttributeError(f'{cls.__name__!r} object has no attribute {name!r}')

    def __setattr__(self, name, value):
        cls = type(self)
        if len(name) == 1:
            error = None
            if name in cls.shortcut_names:
                error = f'readonly attribute {name!r}'
            elif name.islower():
                error = f'can\'t set attributes \'a\' to \'z\' in {cls.__name__}'
            if error:
                raise AttributeError(error)
        super().__setattr__(name, value)

    def __iter__(self):
        return iter(self._components)

    def __len__(self):
        return len(self._components)

    def __getitem__(self, index):
        cls = type(self)
        if isinstance(index, slice):
            return cls(self._components[index])
        elif isinstance(index, numbers.Integral):
            return self._components[index]
        raise TypeError(f'{cls.__name__} indices must be integers')

    def __repr__(self):
        components = reprlib.repr(self._components)
        components = components[components.find('['):-1]
        return 'Vector({})'.format(components)

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return bytes([ord(self.typecode)]) + bytes(self._components)

    def __eq__(self, other):
        if len(self) != len(other):
            return False
        return all(a == b for a, b in zip(self, other))

    def __hash__(self):
        return reduce(operator.xor, map(hash, self._components))

    def __abs__(self):
        return math.sqrt(sum(x * x for x in self))

    def __bool__(self):
        return bool(abs(self))

    def angle(self, n):
        r = math.sqrt(sum(x * x for x in self[n:]))
        a = math.atan2(r, self[n-1])
        if (n == len(self) - 1) and (self[-1] < 0):
            return math.pi * 2 - a
        return a

    def angles(self):
        return (self.angle(n) for n in range(1, len(self)))

    def __format__(self, format_spec=''):
        if format_spec.endswith('h'):
            format_spec = format_spec[:-1]
            coords = itertools.chain([abs(self)], self.angles())
            outer_format = '<({})>'
        else:
            coords = self
            outer_format = '({})'
        components = (format(c, format_spec) for c in coords)
        return outer_format.format(', '.join(components))

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
