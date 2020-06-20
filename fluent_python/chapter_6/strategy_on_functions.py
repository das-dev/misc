import inspect
from collections import namedtuple

from fluent_python.chapter_6 import promotions


class Order:  # the Context

    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = list(cart)
        self.promotion = promotion

    def total(self):
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total

    def due(self):
        if self.promotion is None:
            return self.total()
        return self.total() - self.promotion(self)

    def __repr__(self):
        return f'<Order total: {self.total():.2f} due: {self.due():.2f}'


promos = [func for name, func in inspect.getmembers(promotions, inspect.isfunction)]


def best_promo(order):
    """Select best discount abailable"""

    return max(promo(order) for promo in promos)


Customer = namedtuple('Customer', 'name fidelity')


class LineItem:

    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price

    def total(self):
        return self.price * self.quantity


if __name__ == '__main__':
    joe = Customer('John Doe', 0)
    ann = Customer('Ann Smith', 1100)
    cart = [LineItem('banana', 4, 5),
            LineItem('apple', 10, 1.5),
            LineItem('watermelon', 5, 5.0)]
    print(Order(joe, cart, promotions.fidelity_promo))
    print(Order(ann, cart, promotions.fidelity_promo))
    banana_cart = [LineItem('banana', 30, .5),
                   LineItem('apple', 10, 1.5)]
    print(Order(joe, banana_cart, promotions.bulk_items_promo))
    long_order = [LineItem(str(item_code), 1, 1.0) for item_code in range(10)]
    print(Order(joe, long_order, promotions.large_order_promo))
    print(Order(joe, cart, promotions.large_order_promo))
    print(Order(joe, long_order, best_promo))
    print(Order(joe, banana_cart, best_promo))
    print(Order(ann, cart, best_promo))
