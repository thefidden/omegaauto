from typing import Any

from django.core.management.base import BaseCommand

from cars.models import Car
from utils import set_car_prices


class Command(BaseCommand):
    help = 'Команда для установки значений поля total_price_rub для объектов Car'

    def handle(self, *args: Any, **options: Any) -> str | None:
        cars = Car.objects.all().select_related('fuel')
        cars_count: int = cars.count()

        for ordinal, car in enumerate(cars, start = 1):
            car: Car = car
            set_car_prices(car)
            car.save(update_fields = (
                'price_rub', 'price_poshlina_rub', 'price_sbor_rub', 'price_util_rub', 'price_total_rub'
            ))

            self.stdout.write(f'Установлены стоимости для автомобилей: {ordinal} из {cars_count}')