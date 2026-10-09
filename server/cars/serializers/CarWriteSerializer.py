from rest_framework import serializers
from cars.models import Car, CarImage, Brand, Fuel, Gear, Color, CarStatus


class CarWriteSerializer(serializers.ModelSerializer):
    model = serializers.CharField(max_length = 50)
    year = serializers.IntegerField(min_value = 1970)
    mileage = serializers.IntegerField(min_value = 0)
    power = serializers.IntegerField(min_value = 0)
    displacement = serializers.DecimalField(max_digits = 2, decimal_places = 1)
    vin = serializers.CharField(required = False, max_length = 20, allow_blank = True)
    price = serializers.IntegerField()

    brand = serializers.SlugRelatedField(queryset = Brand.objects.all(), slug_field = 'name')
    fuel = serializers.SlugRelatedField(queryset = Fuel.objects.all(), slug_field = 'name')
    gear = serializers.SlugRelatedField(queryset = Gear.objects.all(), slug_field = 'name')
    color = serializers.SlugRelatedField(queryset = Color.objects.all(), slug_field = 'name')
    status = serializers.SlugRelatedField(queryset = CarStatus.objects.all(), slug_field = 'name')

    images = serializers.ListField(
        child = serializers.ImageField(allow_empty_file = True, use_url = False),
        required = False
    )

    class Meta:
        model = Car
        fields = (
            'model', 'brand', 'year', 'mileage', 'power', 'displacement', 'vin', 'price', 'fuel',
            'gear', 'color', 'status', 'images', 'created_at', 'updated_at'
        )

    def create(self, validated_data: dict) -> Car:
        images = validated_data.pop('images', [])
        car = Car.objects.create(**validated_data)

        for index, image in enumerate(images):
            CarImage.objects.create(car = car, image = image, index = index)

        return car
