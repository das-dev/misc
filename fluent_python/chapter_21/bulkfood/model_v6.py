import abc


class AutoStorage:
    __counter = 0

    def __init__(self):
        self.storage_name = f'_{self.__class__.__name__}#{self.__counter}'
        self.__class__.__counter += 1

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        setattr(instance, self.storage_name, value)


class Validated(abc.ABC, AutoStorage):
    def __set__(self, instance, value):
        value = self.validate(instance, value)
        super().__set__(instance, value)

    @abc.abstractmethod
    def validate(self, instance, value):
        """ return validated value or raise ValueError """


class Quantity(Validated):
    def validate(self, instance, value):
        if value <= 0:
            raise ValueError('value must be > 0')
        return value


class NonBlank(Validated):
    def validate(self, instance, value):
        if not isinstance(value, str):
            raise ValueError('value must be a string')
        value = value.strip()
        if not value:
            raise ValueError('value must be empty or blank')
        return value


def entity(cls):
    for key, attr in cls.__dict__.items():
        if isinstance(attr, Validated):
            attr.storage_name = f'_{type(attr).__name__}#{key}'
    return cls
