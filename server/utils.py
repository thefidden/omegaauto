import logging
import os
import datetime
import threading
from time import sleep

from django.db import transaction

from cars.models import Car, CarImage
from currencies import convert

# Если месяц выпуска неизвестен — по международным правилам принимается 1 июля.
DEFAULT_MANUFACTURE_MONTH = 7


def get_image_upload_path(instance: CarImage, filename) -> str:
    ext = os.path.splitext(filename)[1].lower()
    if ext not in {'.jpg', '.jpeg', '.png', '.webp'}:
        ext = '.webp'
    return os.path.join('car-images', str(instance.car_id), f'{instance.index}{ext}')


def get_car_age(car: Car, as_of: datetime.date | None = None) -> int:
    """
    Полных лет автомобиля на дату as_of (по умолчанию — сегодня).

    По правилам растаможки возраст увеличивается на 1 год 15-го числа месяца выпуска.
    Пример: выпуск ноябрь 2018 → 3 полных года с 15.11.2021 (категория «от 3 до 5»),
    5 полных лет с 15.11.2023 (категория «старше 5»).

    Месяц берётся из car.manufacture_month, если поле есть и задано;
    иначе — июль (DEFAULT_MANUFACTURE_MONTH).
    """
    as_of = as_of or datetime.date.today()
    month = getattr(car, 'manufacture_month', None) or DEFAULT_MANUFACTURE_MONTH

    age = as_of.year - car.year
    if (as_of.month, as_of.day) < (month, 15):
        age -= 1

    return max(age, 0)


def get_car_poshlina(car: Car) -> int:
    """Функция расчета пошлины автомобиля в RUB"""

    result_eur: float = 0

    car_age = get_car_age(car)

    car_price_cny: int = car.price_cny
    car_price_eur: float = convert(car_price_cny, 'CNY', 'EUR')

    car_displacement_cm3: int = int(car.displacement * 1000)
    car_engine: str = car.fuel.name

    if car_engine in {'Бензин', 'Гибрид', 'Дизель'}:
        if car_age < 3:
            if car_price_eur < 8_500:     result_eur = max(car_price_eur * 0.54, car_displacement_cm3 * 2.5)
            elif car_price_eur < 16_700:  result_eur = max(car_price_eur * 0.48, car_displacement_cm3 * 3.5)
            elif car_price_eur < 42_300:  result_eur = max(car_price_eur * 0.48, car_displacement_cm3 * 5.5)
            elif car_price_eur < 84_500:  result_eur = max(car_price_eur * 0.48, car_displacement_cm3 * 7.5)
            elif car_price_eur < 169_000: result_eur = max(car_price_eur * 0.48, car_displacement_cm3 * 15.0)
            else:                         result_eur = max(car_price_eur * 0.48, car_displacement_cm3 * 20.0)

        elif car_age < 5:
            if car_displacement_cm3 <= 1_000:   result_eur = car_displacement_cm3 * 1.5
            elif car_displacement_cm3 <= 1_500: result_eur = car_displacement_cm3 * 1.7
            elif car_displacement_cm3 <= 1_800: result_eur = car_displacement_cm3 * 2.5
            elif car_displacement_cm3 <= 2_300: result_eur = car_displacement_cm3 * 2.7
            elif car_displacement_cm3 <= 3_000: result_eur = car_displacement_cm3 * 3.0
            else:                               result_eur = car_displacement_cm3 * 3.6

        else:
            if car_displacement_cm3 <= 1_000:   result_eur = car_displacement_cm3 * 3.0
            elif car_displacement_cm3 <= 1_500: result_eur = car_displacement_cm3 * 3.2
            elif car_displacement_cm3 <= 1_800: result_eur = car_displacement_cm3 * 3.5
            elif car_displacement_cm3 <= 2_300: result_eur = car_displacement_cm3 * 4.8
            elif car_displacement_cm3 <= 3_000: result_eur = car_displacement_cm3 * 5.0
            else:                               result_eur = car_displacement_cm3 * 5.7

    elif car_engine in {'Электро'}:
        result_eur = car_price_eur * 0.15

    return int(convert(result_eur, 'EUR', 'RUB'))


def get_car_sbor(car: Car) -> int:
    """Функция расчета таможенного сбора автомобиля в RUB"""

    car_price_cny: int = car.price_cny
    car_price_rub: int = int(convert(car_price_cny, 'CNY', 'RUB'))

    if car_price_rub <= 200_000:      return 1_231
    elif car_price_rub <= 450_000:    return 2_462
    elif car_price_rub <= 1_200_000:  return 4_924
    elif car_price_rub <= 2_700_000:  return 13_541
    elif car_price_rub <= 4_200_000:  return 18_465
    elif car_price_rub <= 5_500_000:  return 21_344
    elif car_price_rub <= 10_000_000: return 49_240
    else:                             return 73_860


def get_car_util(car: Car) -> int:
    """Функция расчета утильсбора автомобиля в RUB"""

    car_age = get_car_age(car)
    car_engine: str = car.fuel.name
    car_power: int = car.power
    car_displacement_cm3: int = int(car.displacement * 1000)

    if car_engine in {'Бензин', 'Дизель'}:
        if car_displacement_cm3 <= 1_000:
            if car_age < 3:
                if car_power <= 160:   return 3_400
                elif car_power <= 190: return 307_200
                elif car_power <= 220: return 316_800
                elif car_power <= 250: return 324_000
                else:                  return 345_600
            else:
                if car_power <= 160:   return 5_200
                elif car_power <= 190: return 568_000
                elif car_power <= 220: return 585_600
                elif car_power <= 250: return 602_400
                else:                  return 602_400

        elif car_displacement_cm3 <= 2000:
            if car_age < 3:
                if car_power <= 160:   return 3_400
                elif car_power <= 190: return 900_000
                elif car_power <= 220: return 952_800
                elif car_power <= 250: return 1_010_400
                elif car_power <= 280: return 1_142_400
                elif car_power <= 310: return 1_291_200
                elif car_power <= 340: return 1_459_200
                elif car_power <= 370: return 1_663_200
                elif car_power <= 400: return 1_896_000
                elif car_power <= 430: return 2_160_000
                elif car_power <= 460: return 2_464_800
                elif car_power <= 500: return 2_808_000
                else:                  return 3_201_600
            else:
                if car_power <= 160:   return 5_200
                elif car_power <= 190: return 1_492_800
                elif car_power <= 220: return 1_584_000
                elif car_power <= 250: return 1_677_600
                elif car_power <= 280: return 1_838_400
                elif car_power <= 310: return 2_011_200
                elif car_power <= 340: return 2_203_200
                elif car_power <= 370: return 2_412_000
                elif car_power <= 400: return 2_640_000
                elif car_power <= 430: return 2_892_000
                elif car_power <= 460: return 3_168_000
                elif car_power <= 500: return 3_468_000
                else:                  return 3_796_800

        elif car_displacement_cm3 <= 3_000:
            if car_age < 3:
                if car_power <= 160:   return 3_400
                elif car_power <= 190: return 2_306_800
                elif car_power <= 220: return 2_364_000
                elif car_power <= 250: return 2_402_400
                elif car_power <= 280: return 2_520_000
                elif car_power <= 310: return 2_620_800
                elif car_power <= 340: return 2_726_400
                elif car_power <= 370: return 2_834_400
                elif car_power <= 400: return 2_949_600
                elif car_power <= 430: return 3_067_200
                elif car_power <= 460: return 3_189_600
                elif car_power <= 500: return 3_316_800
                else:                  return 3_448_800
            else:
                if car_power <= 160:   return 5_200
                elif car_power <= 190: return 3_456_000
                elif car_power <= 220: return 3_501_600
                elif car_power <= 250: return 3_552_000
                elif car_power <= 280: return 3_660_000
                elif car_power <= 310: return 3_770_400
                elif car_power <= 340: return 3_873_600
                elif car_power <= 370: return 3_981_600
                elif car_power <= 400: return 4_094_400
                elif car_power <= 430: return 4_209_600
                elif car_power <= 460: return 4_327_200
                elif car_power <= 500: return 4_447_200
                else:                  return 4_572_000

        elif car_displacement_cm3 <= 3_500:
            if car_age < 3:
                if car_power <= 160:   return 2_584_000
                elif car_power <= 190: return 2_635_200
                elif car_power <= 220: return 2_688_000
                elif car_power <= 250: return 2_743_200
                elif car_power <= 280: return 2_810_400
                elif car_power <= 310: return 2_880_000
                elif car_power <= 340: return 3_038_400
                elif car_power <= 370: return 3_206_400
                elif car_power <= 400: return 3_384_000
                elif car_power <= 430: return 3_568_800
                elif car_power <= 460: return 3_765_600
                elif car_power <= 500: return 3_972_000
                else:                  return 4_190_400
            else:
                if car_power <= 160:   return 3_956_200
                elif car_power <= 190: return 4_000_800
                elif car_power <= 220: return 4_044_000
                elif car_power <= 250: return 4_087_200
                elif car_power <= 280: return 4_144_800
                elif car_power <= 310: return 4_248_000
                elif car_power <= 340: return 4_356_000
                elif car_power <= 370: return 4_485_600
                elif car_power <= 400: return 4_620_000
                elif car_power <= 430: return 4_759_200
                elif car_power <= 460: return 4_900_800
                elif car_power <= 500: return 5_049_600
                else:                  return 5_200_800

        else:
            if car_age < 3:
                if car_power <= 160:   return 3_290_600
                elif car_power <= 190: return 3_345_600
                elif car_power <= 220: return 3_403_200
                elif car_power <= 250: return 3_460_800
                elif car_power <= 280: return 3_530_400
                elif car_power <= 310: return 3_600_000
                elif car_power <= 340: return 3_727_200
                elif car_power <= 370: return 3_857_600
                elif car_power <= 400: return 3_993_600
                elif car_power <= 430: return 4_132_800
                elif car_power <= 460: return 4_276_800
                elif car_power <= 500: return 4_425_600
                else:                  return 4_581_600
            else:
                if car_power <= 160:   return 4_325_800
                elif car_power <= 190: return 4_389_600
                elif car_power <= 220: return 4_456_800
                elif car_power <= 250: return 4_524_000
                elif car_power <= 280: return 4_627_200
                elif car_power <= 310: return 4_732_800
                elif car_power <= 340: return 4_992_000
                elif car_power <= 370: return 5_268_000
                elif car_power <= 400: return 5_558_400
                elif car_power <= 430: return 5_863_200
                elif car_power <= 460: return 6_187_200
                elif car_power <= 500: return 6_528_000
                else:                  return 6_885_600

    elif car_engine in {'Электро', 'Гибрид'}:
        if car_age < 3:
            if car_power <= 80:    return 3_400
            elif car_power <= 100: return 991_200
            elif car_power <= 130: return 1_317_600
            elif car_power <= 160: return 1_560_000
            elif car_power <= 190: return 1_848_000
            elif car_power <= 220: return 2_193_600
            elif car_power <= 250: return 2_599_200
            elif car_power <= 280: return 3_079_200
            else:                  return 3_648_000
        else:
            if car_power <= 80:    return 5_200
            elif car_power <= 100: return 1_641_600
            elif car_power <= 130: return 1_912_800
            elif car_power <= 160: return 2_227_200
            elif car_power <= 190: return 2_594_400
            elif car_power <= 220: return 3_024_000
            elif car_power <= 250: return 3_523_200
            elif car_power <= 280: return 4_104_000
            else:                  return 4_780_800

    else:
        return 0


def get_car_total_price(car: Car) -> int:
    price_car_rub: int = int(convert(car.price_cny, 'CNY', 'RUB'))
    price_poshlina: int = int(get_car_poshlina(car))
    price_sbor: int = get_car_sbor(car)
    price_util: int = get_car_util(car)

    return price_car_rub + price_poshlina + price_sbor + price_util


def set_car_prices(car: Car) -> Car:
    car.price_rub = int(convert(car.price_cny, 'CNY', 'RUB'))
    car.price_poshlina_rub = get_car_poshlina(car)
    car.price_sbor_rub = get_car_sbor(car)
    car.price_util_rub = get_car_util(car)
    car.price_total_rub = (
            car.price_rub
            + car.price_poshlina_rub
            + car.price_sbor_rub
            + car.price_util_rub
    )

    return car
