import keyword

from collections import abc

from osconfeed import load


class FrozenJSON:
    """
    >>> raw_feed = load()
    >>> feed = FrozenJSON(load())
    >>> len(feed.Schedule.speakers)
    357
    >>> sorted(feed.Schedule.keys())
    ['conferences', 'events', 'speakers', 'venues']
    >>> for key, value in sorted(feed.Schedule.items()):
    ...     print(f'{len(value):3} {key}')
      1 conferences
    494 events
    357 speakers
     53 venues
    >>> feed.Schedule.speakers[-1].name
    'Carina C. Zona'
    >>> talk = feed.Schedule.events[40]
    >>> type(talk)
    <class 'frozen_json.FrozenJSON'>
    >>> talk.name
    'There *Will* Be Bugs'
    >>> talk.speakers
    [3471, 5199]
    >>> talk.flavor
    Traceback (most recent call last):
    ...
    AttributeError: 'FrozenJSON' object has no attribute 'flavor'
    """

    def __new__(cls, data):
        if isinstance(data, abc.Mapping):
            return super().__new__(cls)
        elif isinstance(data, abc.MutableSequence):
            return [cls(item) for item in data]
        return data

    def __init__(self, mapping):
        self.__data = {}
        for key, value in mapping.items():
            if keyword.iskeyword(key):
                key = f'{key}_'
            self.__data[key] = value

    def __getattr__(self, name):
        cls = type(self)
        if hasattr(self.__data, name):
            return getattr(self.__data, name)
        try:
            return cls(self.__data[name])
        except KeyError:
            msg = f'{cls.__name__!r} object has no attribute {name!r}'
            raise AttributeError(msg)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
