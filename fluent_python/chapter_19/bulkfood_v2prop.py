def quantity(storage_name):
    def qty_getter(instance):
        return instance.__dict__[storage_name]

    def qty_setter(instance, value):
        if value > 0:
            instance.__dict__[storage_name] = value
        else:
            raise ValueError('value must be > 0')
    return property(qty_getter, qty_setter)


class LineItem:
    """
        >>> raisins = LineItem('Golden raisins', 10, 6.95)
        >>> raisins.subtotal()
        69.5
        >>> raisins.weight = -20
        Traceback (most recent call last):
        ...
        ValueError: value must be > 0
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

    weight = quantity('weight')
    price = quantity('price')

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price


if __name__ == '__main__':
    import doctest
    doctest.testmod()
