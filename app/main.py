import datetime
import json

from typing import Any, List, Dict, Tuple

from app.car import Car
from app.customer import Customer
from app.shop import Shop


def load_data() -> Dict[str, Any]:
    with open("app/config.json") as f:
        data = json.load(f)
        return data


def init_customers(data: Dict[str, Any]) -> List[Customer]:
    customers = [
        Customer(
            name=customer["name"],
            product_cart=customer["product_cart"],
            location=customer["location"],
            money=customer["money"],
            car=Car(
                customer["car"]["brand"],
                customer["car"]["fuel_consumption"],
            ),
        )
        for customer in data["customers"]
    ]
    return customers


def init_shops(data: Dict[str, Any]) -> List[Shop]:
    shops = [
        Shop(
            name=shop["name"],
            location=shop["location"],
            products=shop["products"],
        )
        for shop in data["shops"]
    ]
    return shops


def calculate_trip_cost(
    distance: float, customer: Customer, shop: Shop, data: Dict[str, Any]
) -> float:
    way = customer.car.trip_cost(distance * 2, data["FUEL_PRICE"])
    products = shop.calculate_total_cost(customer.product_cart)
    return way + products


def print_trip_summary(
    customer: Customer, shop: Shop, all_sum: Tuple[float, str]
) -> None:
    print(f"{customer.name}'s trip to the {shop.name} costs {all_sum[0]}")


def choose_cheapest_shop(
    shops: List[Shop], all_sum_trip: List[Tuple[float, str]]
) -> Shop:
    chosen_shop_name = all_sum_trip[0][1]
    chosen_shop = next(
        shop for shop in shops if shop.name == chosen_shop_name
    )
    return chosen_shop


def print_way_to_shop(customer: Customer, chosen_shop: Shop) -> None:
    print(f"{customer.name} rides to {chosen_shop.name}\n")


def print_way_to_home(customer: Customer) -> None:
    print(f"{customer.name} rides home")


def show_receipt(customer: Customer, chosen_shop: Shop) -> None:
    print("Date:", datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    print(f"Thanks, {customer.name}, for your purchase!")
    print("You have bought:")
    total = 0
    for product, amount in customer.product_cart.items():
        if product in chosen_shop.products:
            product_name = product if amount == 1 else product + "s"
            if (chosen_shop.products[product] * amount) == int(
                chosen_shop.products[product] * amount
            ):
                print(
                    f"{amount} {product_name} for "
                    f"{int(chosen_shop.products[product] * amount)} "
                    f"dollars"
                )
            else:
                print(
                    f"{amount} {product_name} for "
                    f"{chosen_shop.products[product] * amount} dollars"
                )
            total += chosen_shop.products[product] * amount
    print(f"Total cost is {total} dollars")
    print("See you again!\n")


def shop_trip() -> None:
    data = load_data()
    customers = init_customers(data)
    shops = init_shops(data)

    for customer in customers:
        print(f"{customer.name} has {customer.money} dollars")

        all_sum_trip = []
        for shop in shops:
            distance = customer.calculate_distance(shop.location)
            all_sum = (
                calculate_trip_cost(distance, customer, shop, data),
                shop.name,
            )
            all_sum_trip.append(all_sum)
            print_trip_summary(customer, shop, all_sum)

        all_sum_trip = sorted(all_sum_trip)
        if customer.money > all_sum_trip[0][0]:
            chosen_shop = choose_cheapest_shop(shops, all_sum_trip)
            print_way_to_shop(customer, chosen_shop)
            show_receipt(customer, chosen_shop)
            print_way_to_home(customer)
            customer.money -= all_sum_trip[0][0]
            print(f"{customer.name} now has {customer.money} dollars\n")
        else:
            print(
                f"{customer.name} doesn't have enough money"
                f" to make a purchase in any shop"
            )


shop_trip()
