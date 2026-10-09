from rest_framework import serializers

from telegram_bot.models import TelegramCarCard

class TelegramCarCardSerializer(serializers.ModelSerializer):
    car = serializers.CharField(source = 'car.model')

    class Meta:
        model = TelegramCarCard
        fields = ('id', 'car', 'text', 'link')
