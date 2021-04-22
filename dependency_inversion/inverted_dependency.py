from dataclasses import dataclass
from decimal import Decimal
from typing import List


@dataclass
class Product:
    cost: Decimal
    name: str
    count: int


class ProductStorage:
    @property
    def products(self) -> List[Product]:
        raise NotImplementedError


class DiscountCalculator:
    def get_discount(self, product: Product) -> Decimal:
        raise NotImplementedError


class Warehouse(ProductStorage):

    @property
    def products(self):
        return [
            Product(Decimal(100), 'Tyres', 1000),
            Product(Decimal(120), 'Disks', 200),
            Product(Decimal(90), 'Alarms', 500),
            Product(Decimal(150), 'Batteries', 200),
            Product(Decimal(60), 'Tools', 50),
        ]


class SimpleScheme(DiscountCalculator):
    DISCOUNTS = {
        'Tyres': 0.01,
        'Disks': 0.05,
        'Alarms': 0.1,
        'Batteries': 0.15,
        'Tools': 0.1
    }

    def get_discount(self, product: Product):
        return Decimal(str(self.DISCOUNTS.get(product.name, 0)))


class ProductService:
    def get_all_discounts(self, storage: ProductStorage, calculator: DiscountCalculator) -> Decimal:
        return sum(p.cost * p.count * calculator.get_discount(p)
                   for p in storage.products)


if __name__ == '__main__':
    service = ProductService()
    total = service.get_all_discounts(Warehouse(), SimpleScheme())
    print(f'Discount for all products = {total}')
