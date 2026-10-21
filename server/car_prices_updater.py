import logging
import os
import sys
import threading
import time

from django.db import transaction

import currencies
from cars.models import Car
from utils import set_car_prices

_INTERVAL: int = 60 * 60 * 24
_started: bool = False
_logger = logging.getLogger(__name__)


def _update_car_prices() -> None:
    try:
        for car in Car.objects.all().select_related('fuel'):
            with transaction.atomic():
                car: Car = car
                set_car_prices(car)
                car.save(update_fields = (
                    'price_rub', 'price_poshlina_rub', 'price_sbor_rub', 'price_util_rub', 'price_total_rub'
                ))
    except Exception:
        _logger.exception('Ошибка обновления цен для автомобилей')

    _logger.info('Обновлены цены для автомобилей')


def _should_run_updater() -> bool:
    skip = {'migrate', 'makemigrations', 'test', 'shell', 'collectstatic', 'createsuperuser'}

    if any(cmd in sys.argv for cmd in skip):
        return False

    if 'runserver' in sys.argv and os.environ.get('RUN_MAIN') != 'true':
        return False

    return True


def start_background_updates() -> None:
    global _started

    def func() -> None:
        while _started:
            currencies.load_rates_from_cbr()
            _update_car_prices()
            time.sleep(_INTERVAL)

    if _started or not _should_run_updater():
        return

    _started = True
    threading.Thread(target = func, name = 'car-prices-updater', daemon = True).start()
