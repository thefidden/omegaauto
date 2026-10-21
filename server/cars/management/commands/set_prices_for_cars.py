from typing import Any

from django.core.management.base import BaseCommand

from cars.models import Car
from currencies import convert
from utils import get_car_poshlina, get_car_sbor, get_car_util


class Command(BaseCommand):
    help = (
        'Recalculate age-dependent car prices (price_poshlina_rub, price_util_rub) '
        'and refresh price_total_rub for all cars'
    )

    def handle(self, *args: Any, **options: Any) -> None:
        cars = Car.objects.all().select_related('fuel')
        total_to_handle = cars.count()
        updated = 0

        for index, car in enumerate(cars.iterator(), start = 1):
            car.price_rub = int(convert(car.price_cny, 'CNY', 'RUB'))
            car.price_sbor_rub = get_car_sbor(car)
            car.price_poshlina_rub = int(get_car_poshlina(car))
            car.price_util_rub = get_car_util(car)
            car.price_total_rub = (
                car.price_rub
                + car.price_poshlina_rub
                + car.price_sbor_rub
                + car.price_util_rub
            )

            car.save(update_fields = (
                'price_rub', 'price_poshlina_rub', 'price_sbor_rub', 'price_util_rub',
                'price_total_rub', 'updated_at'
            ))
            updated += 1
            self.stdout.write(f'Обработано: {index} из {total_to_handle}')

        self.stdout.write(self.style.SUCCESS(f'Пересчитано автомобилей: {updated}'))
