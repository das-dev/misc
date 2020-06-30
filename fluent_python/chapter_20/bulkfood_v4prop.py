def quantity():
    try:
        quantity.counter += 1
    except AttributeError:
        quantity.counter = 0

    storage_name = f'_quantity:{quantity.counter}'

    def qty_getter(instance):
        return getattr(instance, storage_name)

    def qty_setter(instance, value):
        if value > 0:
            setattr(instance, storage_name, value)
        else:
            raise ValueError('value must be > 0')

    return property(qty_getter, qty_setter)


class LineItem:
    """
        >>> LineItem.weight  # doctest:+ELLIPSIS
        <property object at ...
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

    weight = quantity()
    price = quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price


if __name__ == '__main__':
    import doctest
    doctest.testmod()
