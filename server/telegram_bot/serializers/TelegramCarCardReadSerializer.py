from rest_framework import serializers

from telegram_bot.models import TelegramCarCard


class TelegramCarCardReadSerializer(serializers.ModelSerializer):
    car = serializers.SerializerMethodField()
    link = serializers.CharField(max_length = 100)

    class Meta:
        model = TelegramCarCard
        fields = ('id', 'car', 'link')

    def get_car(self, obj: TelegramCarCard):
        return f'{obj.car.brand} {obj.car.model}'
