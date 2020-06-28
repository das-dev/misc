import warnings
import osconfeed
import shelve


DB_NAME = 'data/schedule_db'
CONFERENCE = 'conference.115'


class Record:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def load_db(db):
    """
    >>> import shelve
    >>> db = shelve.open(DB_NAME)
    >>> if CONFERENCE not in db:
    ...     load_db(db)
    >>> speaker = db['speaker.3471']
    >>> type(speaker)
    <class 'schedule.Record'>
    >>> speaker.name, speaker.twitter
    ('Anna Ravenscroft', 'annaraven')
    >>> db.close()
    """
    raw_data = osconfeed.load()
    warnings.warn('loading ' + DB_NAME)
    for collection, records in raw_data['Schedule'].items():
        record_type = collection[:-1]
        for record in records:
            key = '{}.{}'.format(record_type, record['serial'])
            record['serial'] = key
            db[key] = Record(**record)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

