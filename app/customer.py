import math
import dataclasses
from app.car import Car


@dataclasses.dataclass
class Customer:
    name: str
    product_cart: dict
    location: list[int, int]
    money: float
    car: Car

    def calculate_distance(self, shop_location: list[int, int]) -> float:
        return math.sqrt(
            (shop_location[0] - self.location[0]) ** 2
            + (shop_location[1] - self.location[1]) ** 2
        )
