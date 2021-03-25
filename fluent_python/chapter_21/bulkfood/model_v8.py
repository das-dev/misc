import abc
import collections


class AutoStorage:
    __counter = 0

    def __init__(self):
        cls = self.__class__
        self.storage_name = f'_{cls.__name__}#{cls.__counter}'
        cls.__counter += 1

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        setattr(instance, self.storage_name, value)


class Validated(abc.ABC, AutoStorage):

    def __set__(self, instance, value):
        value = self.validate(instance, value)
        super().__set__(instance, value)

    @abc.abstractmethod
    def validate(self, instance, value):
        """return validated value or raise ValueError"""


class Quantity(Validated):
    """a number greater than zero"""

    def validate(self, instance, value):
        if value <= 0:
            raise ValueError('value must be > 0')
        return value


class NonBlank(Validated):
    """a string with at least one non-space character"""

    def validate(self, instance, value):
        try:
            value = value.strip()
        except AttributeError:
            raise ValueError('value must be a string')
        if len(value) == 0:
            raise ValueError('value cannot be empty or blank')
        return value


class EntityMeta(type):
    """Metaclass for business entities with validated fields"""

    @classmethod
    def __prepare__(cls, name, bases):
        return collections.OrderedDict()

    def __init__(cls, name, bases, attr_dict):
        super().__init__(name, bases, attr_dict)
        cls._field_names = []
        for key, attr in attr_dict.items():
            if isinstance(attr, Validated):
                attr.storage_name = f'_{type(attr).__name__}#{key}'
                cls._field_names.append(key)


class Entity(metaclass=EntityMeta):
    """ Business entity with validated fields """

    @classmethod
    def field_names(cls):
        for name in cls._field_names:
            yield name
