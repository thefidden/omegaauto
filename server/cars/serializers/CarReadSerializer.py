from rest_framework import serializers

from cars.models import Car
from cars.serializers.CarImageSerizalier import CarImageSerializer


class CarReadSerializer(serializers.ModelSerializer):
    fuel = serializers.CharField(source = 'fuel.name', read_only = True)
    gear = serializers.CharField(source = 'gear.name', read_only = True)
    color = serializers.CharField(source = 'color.name', read_only = True)
    status = serializers.CharField(source = 'status.name', read_only = True)
    brand = serializers.CharField(source = 'brand.name', read_only = True)
    vin = serializers.CharField(max_length = 20, required = False, allow_blank = True, read_only = True)
    year = serializers.IntegerField(source = 'release_date.year', read_only = True)
    images = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = Car
        fields = (
            'id', 'model', 'brand', 'release_date', 'year', 'mileage', 'power', 'displacement', 'vin', 'fuel', 'gear',
            'price_cny', 'price_rub', 'price_poshlina_rub', 'price_sbor_rub', 'price_util_rub', 'price_total_rub',
            'color', 'status', 'images', 'created_at', 'updated_at'
        )
        read_only_fields = (
            'id', 'model', 'brand', 'release_date', 'year', 'mileage', 'power', 'displacement', 'vin', 'fuel', 'gear',
            'price_cny', 'price_rub', 'price_poshlina_rub', 'price_sbor_rub', 'price_util_rub', 'price_total_rub',
            'color', 'status', 'images', 'created_at', 'updated_at'
        )

    def get_images(self, obj: Car) -> list:
        return CarImageSerializer(obj.images.all(), many = True).data
