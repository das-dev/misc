from dataclasses import dataclass
from decimal import Decimal
from typing import List


@dataclass
class Product:
    cost: Decimal
    name: str
    count: int


class Warehouse:
    def __init__(self) -> None:
        self.products = self._make_products()

    @staticmethod
    def _make_products() -> List[Product]:
        return [
            Product(Decimal('100'), 'Tyres', 1000),
            Product(Decimal('120'), 'Disks', 200),
            Product(Decimal('90'), 'Alarms', 500),
            Product(Decimal('150'), 'Batteries', 200),
            Product(Decimal('60'), 'Tools', 50),
        ]


class DiscountScheme:
    DISCOUNTS = {
        'Tyres': 0.01,
        'Disks': 0.05,
        'Alarms': 0.1,
        'Batteries': 0.15,
        'Tools': 0.1
    }

    def get_discount(self, product: Product) -> Decimal:
        return Decimal(str(self.DISCOUNTS.get(product.name, 0)))


class ProductService:
    def get_all_discounts(self) -> Decimal:
        scheme = DiscountScheme()
        return sum(p.cost * p.count * scheme.get_discount(p)
                   for p in Warehouse().products)


if __name__ == '__main__':
    service = ProductService()
    print(f'Discount for all products = {service.get_all_discounts()}')
