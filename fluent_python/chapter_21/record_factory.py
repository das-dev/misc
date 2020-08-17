"""
    >>> Dog = record_factory('Dog', 'name weight owner')
    >>> rex = Dog('Rex', 30, 'Bob')
    >>> rex
    Dog(name='Rex', weight=30, owner='Bob')
    >>> name, weight, _ = rex
    >>> name, weight
    ('Rex', 30)
    >>> "{2}'s dog weighs {1}kg".format(*rex)
    "Bob's dog weighs 30kg"
    >>> rex.weight = 32
    >>> rex
    Dog(name='Rex', weight=32, owner='Bob')
    >>> Dog.__mro__
    (<class 'record_factory.Dog'>, <class 'object'>)
"""


def record_factory(classname, fields):
    def __init__(self, *args, **kwargs):
        attrs = dict(zip(self.__slots__, args))
        attrs.update(kwargs)
        for name, value in attrs.items():
            setattr(self, name, value)

    def __iter__(self):
        for field in self.__slots__:
            yield getattr(self, field)

    def __repr__(self):
        params = ', '.join(f'{k}={v!r}' for k, v in zip(self.__slots__, self))
        return f'{self.__class__.__name__}({params})'

    try:
        fields = fields.replace(',', ' ').split()
    except AttributeError:
        pass

    cls_attrs = {
        '__slots__': tuple(fields),
        '__init__': __init__,
        '__iter__': __iter__,
        '__repr__': __repr__
    }
    return type(classname, (object, ), cls_attrs)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
