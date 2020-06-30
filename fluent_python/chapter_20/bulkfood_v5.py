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


class LineItem:
    """
        >>> LineItem.weight  # doctest:+ELLIPSIS
        <bulkfood_v5.Quantity object at ...
        >>> raisins = LineItem('Golden raisins', 10, 6.95)
        >>> raisins.weight
        10
        >>> raisins.price
        6.95
        >>> raisins.subtotal()
        69.5
        >>> raisins.weight = -20
        Traceback (most recent call last):
        ...
        ValueError: value must be > 0
        >>> raisins.description
        'Golden raisins'
        >>> raisins.description = ''
        Traceback (most recent call last):
        ...
        ValueError: value must be empty or blank
        >>> LineItem('', 10, 6.95)
        Traceback (most recent call last):
        ...
        ValueError: value must be empty or blank
        >>> LineItem(0, 10, 6.95)
        Traceback (most recent call last):
        ...
        ValueError: value must be a string
        >>> LineItem('walnuts', 0, 10.0)
        Traceback (most recent call last):
        ...
        ValueError: value must be > 0
        >>> raisins.weight = -20
        Traceback (most recent call last):
        ...
        ValueError: value must be > 0
        >>> LineItem('walnuts', 0, 10.0)
        Traceback (most recent call last):
        ...
        ValueError: value must be > 0
    """

    weight = Quantity()
    price = Quantity()
    description = NonBlank()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price


if __name__ == '__main__':
    import doctest
    doctest.testmod()
