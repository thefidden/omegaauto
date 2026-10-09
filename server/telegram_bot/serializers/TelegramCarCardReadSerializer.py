from rest_framework import serializers

from telegram_bot.models import TelegramCarCard
from cars.models import Car

class TelegramCarCardWriteSerializer(serializers.ModelSerializer):
    car = serializers.PrimaryKeyRelatedField(queryset = Car.objects.all())
    link = serializers.CharField(max_length = 100)

    class Meta:
        model = TelegramCarCard
        fields = ('car', 'link')
