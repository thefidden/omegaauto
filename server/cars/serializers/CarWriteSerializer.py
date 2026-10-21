from django.db import transaction
from rest_framework import serializers

from cars.models import Car, CarImage, Brand, Fuel, Gear, Color, CarStatus
from utils import set_car_prices


class CarWriteSerializer(serializers.ModelSerializer):
    model = serializers.CharField(max_length = 50)
    year = serializers.IntegerField(min_value = 1970)
    mileage = serializers.IntegerField(min_value = 0)
    power = serializers.IntegerField(min_value = 0)
    displacement = serializers.DecimalField(max_digits = 2, decimal_places = 1)
    vin = serializers.CharField(required = False, max_length = 20, allow_blank = True)
    price_cny = serializers.IntegerField()

    brand = serializers.SlugRelatedField(queryset = Brand.objects.all(), slug_field = 'name')
    fuel = serializers.SlugRelatedField(queryset = Fuel.objects.all(), slug_field = 'name')
    gear = serializers.SlugRelatedField(queryset = Gear.objects.all(), slug_field = 'name')
    color = serializers.SlugRelatedField(queryset = Color.objects.all(), slug_field = 'name')
    status = serializers.SlugRelatedField(queryset = CarStatus.objects.all(), slug_field = 'name')

    images = serializers.ListField(
        child = serializers.ImageField(allow_empty_file = True, use_url = False),
        required = False,
        write_only = True
    )

    class Meta:
        model = Car
        fields = (
            'model', 'brand', 'year', 'mileage', 'power', 'displacement', 'vin',
            'price_cny', 'fuel', 'gear', 'color', 'status', 'images', 'created_at', 'updated_at'
        )

    def create(self, validated_data: dict) -> Car:
        images = validated_data.pop('images', [])

        with transaction.atomic():
            car = Car(**validated_data)
            set_car_prices(car)
            car.save()

            for index, image in enumerate(images):
                CarImage.objects.create(car = car, image = image, index = index)

        return car

    def update(self, instance: Car, validated_data: dict) -> Car:
        images = validated_data.pop('images', [])

        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            if {'price_cny', 'year', 'fuel', 'power', 'displacement'} & set(validated_data):
                set_car_prices(instance)

            instance.save()

            if images:
                CarImage.objects.filter(car = instance).delete()

                for index, image in enumerate(images):
                    CarImage.objects.create(car = instance, image = image, index = index)

        return instance
