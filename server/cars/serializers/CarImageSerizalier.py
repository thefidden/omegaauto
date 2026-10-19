from rest_framework import serializers
from cars.models import CarImage, Car


class CarImageSerializer(serializers.ModelSerializer):
    car = serializers.PrimaryKeyRelatedField(queryset = Car.objects.all())

    class Meta:
        model = CarImage
        fields = ('image', 'public', 'index', 'car')
