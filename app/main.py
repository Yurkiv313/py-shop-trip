import datetime
import json

from app.car import Car
from app.customer import Customer
from app.shop import Shop


def shop_trip() -> None:
    with open("app/config.json") as f:
        data = json.load(f)

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

    shops = [
        Shop(
            name=shop["name"],
            location=shop["location"],
            products=shop["products"],
        )
        for shop in data["shops"]
    ]

    for customer in customers:
        print(f"{customer.name} has {customer.money} dollars")

        all_sum_trip = []
        for shop in shops:
            distance = customer.calculate_distance(shop.location)
            way = customer.car.trip_cost(distance * 2, data["FUEL_PRICE"])
            food = shop.calculate_total_cost(customer.product_cart)
            all_sum = (way + food, shop.name)
            all_sum_trip.append(all_sum)

            print(
                f"{customer.name}'s trip to the {shop.name} costs {all_sum[0]}"
            )

        all_sum_trip = sorted(all_sum_trip)
        if customer.money > all_sum_trip[0][0]:
            chosen_shop_name = all_sum_trip[0][1]
            chosen_shop = next(
                shop for shop in shops if shop.name == chosen_shop_name
            )
            print(f"{customer.name} rides to {all_sum_trip[0][1]}\n")
            print(
                "Date:", datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            )
            print(f"Thanks, {customer.name}, for your purchase!")
            print("You have bought:")

            total = 0
            for product, amount in customer.product_cart.items():
                if product in chosen_shop.products:
                    product_name = product if amount == 1 else product + "s"
                    if ((chosen_shop.products[product] * amount)
                            == int(chosen_shop.products[product] * amount)):
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
            print(f"{customer.name} rides home")
            print(
                f"{customer.name} now has "
                f"{customer.money - all_sum_trip[0][0]} dollars\n"
            )
        else:
            print(
                f"{customer.name} doesn't have enough money"
                f" to make a purchase in any shop"
            )
