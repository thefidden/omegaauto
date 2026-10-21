from rest_framework import serializers
from cars.models import Model


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ('name', 'brand')
