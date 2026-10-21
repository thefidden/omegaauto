from typing import Any

from django.core.management.base import BaseCommand

import currencies
from cars.models import Car
from utils import get_car_poshlina, get_car_sbor, get_car_util


class Command(BaseCommand):
    help = 'Команда для установки значений поля total_price_rub для объектов Car'

    def handle(self, *args: Any, **options: Any) -> str | None:
        cars = Car.objects.all().select_related('fuel')
        cars_count: int = cars.count()

        for ordinal, car in enumerate(cars, start = 1):
            car: Car = car
            car.price_rub = currencies.convert(car.price_cny, 'CNY', 'RUB')
            car.price_poshlina_rub = get_car_poshlina(car)
            car.price_sbor_rub = get_car_sbor(car)
            car.price_util_rub = get_car_util(car)
            car.price_total_rub = (
                    car.price_rub
                    + car.price_poshlina_rub
                    + car.price_sbor_rub
                    + car.price_util_rub
            )
            car.save(update_fields = (
                'price_rub', 'price_poshlina_rub', 'price_sbor_rub', 'price_util_rub', 'price_total_rub'
            ))

            self.stdout.write(f'Установлены стоимости для автомобилей: {ordinal} из {cars_count}')