from rest_framework import serializers

from cars.models import Car
from cars.serializers import CarImageSerializer


class CarReadSerializer(serializers.ModelSerializer):
    fuel = serializers.CharField(source = 'fuel.name')
    gear = serializers.CharField(source = 'gear.name')
    color = serializers.CharField(source = 'color.name')
    status = serializers.CharField(source = 'status.name')
    brand = serializers.CharField(source = 'brand.name')
    vin = serializers.CharField(max_length = 20, required = False, allow_blank = True)
    images = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = (
            'id', 'model', 'brand', 'year', 'mileage', 'power', 'displacement', 'vin', 'fuel', 'gear', 'color',
            'price', 'status', 'images', 'created_at', 'updated_at'
        )

    def get_images(self, obj: Car) -> dict:
        qs = obj.images.all()
        return CarImageSerializer(qs, many = True).data
