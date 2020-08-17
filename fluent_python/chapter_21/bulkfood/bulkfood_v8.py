"""
    >>> LineItem.weight  # doctest:+ELLIPSIS
    <model_v8.Quantity object at ...
    >>> LineItem.weight.storage_name
    '_Quantity#weight'
    >>> raisins = LineItem('Golden raisins', 10, 6.95)
    >>> dir(raisins)[:3]
    ['_NonBlank#description', '_Quantity#price', '_Quantity#weight']
    >>> getattr(raisins, '_NonBlank#description')
    'Golden raisins'
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
    ValueError: value cannot be empty or blank
    >>> LineItem('', 10, 6.95)
    Traceback (most recent call last):
    ...
    ValueError: value cannot be empty or blank
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
    >>> for name in LineItem.field_names():
    ...     print(name)
    description
    weight
    price
"""

import model_v8 as model


class LineItem(model.Entity):
    description = model.NonBlank()
    weight = model.Quantity()
    price = model.Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price


if __name__ == '__main__':
    import doctest
    doctest.testmod()
