class LineItem:
    """
        >>> raisins = LineItem('Golden raisins', 10, 6.95)
        >>> raisins.subtotal()
        69.5
        >>> raisins.weight = -20
        >>> raisins.subtotal()
        -139.0
    """
    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price


if __name__ == '__main__':
    import doctest
    doctest.testmod()
