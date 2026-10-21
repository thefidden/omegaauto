from rest_framework import serializers

from cars.filters import CarImageFilter
from cars.models import Car
from cars.serializers import CarImageSerializer
from utils import get_car_total_price


class ClientCarSerializer(serializers.ModelSerializer):
    fuel = serializers.CharField(source = 'fuel.name', read_only = True)
    gear = serializers.CharField(source = 'gear.name', read_only = True)
    color = serializers.CharField(source = 'color.name', read_only = True)
    status = serializers.CharField(source = 'status.name', read_only = True)
    brand = serializers.CharField(source = 'brand.name', read_only = True)
    images = serializers.SerializerMethodField(read_only = True)
    year = serializers.IntegerField(source = 'release_date.year', read_only = True)
    price_total_rub = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = (
            'id', 'model', 'brand', 'year', 'mileage', 'power', 'displacement', 'fuel', 'gear', 'color',
            'price_total_rub', 'status', 'images'
        )
        read_only_fields = (
            'id', 'model', 'brand', 'year', 'mileage', 'power', 'displacement', 'fuel', 'gear', 'color',
            'price_total_rub', 'status', 'images'
        )

    def get_images(self, obj: Car) -> dict:
        qs = CarImageFilter(data = {'only_public': True}, queryset = obj.images.all()).qs
        return CarImageSerializer(qs, many = True).data

    def get_price_total_rub(self, car: Car) -> int:
        return get_car_total_price(car)
