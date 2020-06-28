"""
    >>> import shelve
    >>> db = shelve.open(DB_NAME)
    >>> if CONFERENCE not in db:
    ...     load_db(db)
    >>> DbRecord.set_db(db)  # <1>
    >>> event = DbRecord.fetch('event.33950')  # <2>
    >>> event  # <3>
    <Event 'There *Will* Be Bugs'>
    >>> event.venue  # <4>
    <DbRecord serial='venue.1449'>
    >>> event.venue.name  # <5>
    'Portland 251'
    >>> for spkr in event.speakers:  # <6>
    ...     print('{0.serial}: {0.name}'.format(spkr))
    ...
    speaker.3471: Anna Ravenscroft
    speaker.5199: Alex Martelli
    >>> db.close()
"""

import warnings
import inspect

import osconfeed

DB_NAME = 'data/schedule2_db'
CONFERENCE = 'conference.115'


class Record:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __eq__(self, other):
        if isinstance(other, Record):
            return self.__dict__ == other.__dict__
        return NotImplemented


class MissingDatabaseError(RuntimeError):
    """Raised when a database is required but was not set"""


class DbRecord(Record):
    __db = None

    @staticmethod
    def set_db(db):
        DbRecord.__db = db

    @staticmethod
    def get_db():
        return DbRecord.__db

    @classmethod
    def fetch(cls, ident):
        db = cls.get_db()
        try:
            return db[ident]
        except TypeError:
            if db is None:
                msg = f'database not set; call \'{cls.__name__}.set_db(my_db)\''
                raise MissingDatabaseError(msg)
            raise

    def __repr__(self):
        if hasattr(self, 'serial'):
            cls_name = type(self).__name__
            return f'<{cls_name} serial={self.serial!r}>'


class Event(DbRecord):
    @property
    def venue(self):
        key = f'venue.{self.venue_serial}'
        return type(self).fetch(key)

    @property
    def speakers(self):
        if not hasattr(self, '_speaker_objs'):
            spkr_serials = self.__dict__['speakers']
            fetch = type(self).fetch
            self._speaker_objs = [fetch(f'speaker.{key}') for key in spkr_serials]
        return self._speaker_objs

    def __repr__(self):
        if hasattr(self, 'name'):
            cls_name = type(self).__name__
            return f'<{cls_name} {self.name!r}>'
        return super().__repr__()


def load_db(db):
    raw_data = osconfeed.load()
    warnings.warn('loading ' + DB_NAME)
    for collection, records in raw_data['Schedule'].items():
        record_type = collection[:-1]
        cls_name = record_type.capitalize()
        cls = globals().get(cls_name, DbRecord)
        if inspect.isclass(cls) and issubclass(cls, DbRecord):
            factory = cls
        else:
            factory = DbRecord
        for record in records:
            key = f"{record_type}.{record['serial']}"
            record['serial'] = key
            print(record)
            db[key] = factory(**record)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
