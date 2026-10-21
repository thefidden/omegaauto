from rest_framework import serializers

import currencies
from cars.models import Car
from cars.serializers.CarImageSerizalier import CarImageSerializer
from utils import get_car_poshlina, get_car_sbor, get_car_util, get_car_total_price


class CarReadSerializer(serializers.ModelSerializer):
    fuel = serializers.CharField(source = 'fuel.name', read_only = True)
    gear = serializers.CharField(source = 'gear.name', read_only = True)
    color = serializers.CharField(source = 'color.name', read_only = True)
    status = serializers.CharField(source = 'status.name', read_only = True)
    brand = serializers.CharField(source = 'brand.name', read_only = True)
    vin = serializers.CharField(max_length = 20, required = False, allow_blank = True, read_only = True)
    images = serializers.SerializerMethodField(read_only = True)

    price_rub = serializers.SerializerMethodField()
    price_poshlina_rub = serializers.SerializerMethodField()
    price_sbor_rub = serializers.SerializerMethodField()
    price_util_rub = serializers.SerializerMethodField()
    price_total_rub = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = (
            'id', 'model', 'brand', 'year', 'mileage', 'power', 'displacement', 'vin', 'fuel', 'gear', 'color',
            'price_cny', 'price_rub', 'price_poshlina_rub', 'price_sbor_rub', 'price_util_rub', 'price_total_rub',
            'status', 'images', 'created_at', 'updated_at'
        )
        read_only_fields = (
            'id', 'model', 'brand', 'year', 'mileage', 'power', 'displacement', 'vin', 'fuel', 'gear', 'color',
            'price_cny', 'price_rub', 'price_poshlina_rub', 'price_sbor_rub', 'price_util_rub', 'price_total_rub',
            'status', 'images', 'created_at', 'updated_at'
        )

    def get_images(self, car: Car) -> list:
        return CarImageSerializer(car.images.all(), many = True).data

    def get_price_rub(self, car: Car) -> int:
        return int(currencies.convert(car.price_cny, 'CNY', 'RUB'))

    def get_price_poshlina_rub(self, car: Car) -> int:
        return int(get_car_poshlina(car))

    def get_price_sbor_rub(self, car: Car) -> int:
        return get_car_sbor(car)

    def get_price_util_rub(self, car: Car) -> int:
        return get_car_util(car)

    def get_price_total_rub(self, car: Car) -> int:
        return get_car_total_price(car)