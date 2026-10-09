from django.db import models


class TelegramCarCard(models.Model):
    objects = models.Manager()

    car = models.ForeignKey('cars.Car', on_delete = models.CASCADE, verbose_name = 'Автомобиль',
                            related_name = 'telegram_card')
    link = models.CharField(max_length = 50, verbose_name = 'Ссылка на сообщение', unique = True)

    created_at = models.DateTimeField(auto_now_add = True, verbose_name = 'Дата создания')
    updated_at = models.DateTimeField(auto_now = True, verbose_name = 'Дата обновления')

    class Meta:
        verbose_name = 'Карточка автомобиля в Telegram'
        verbose_name_plural = 'Карточки автомобилей в Telegram'

    def __str__(self):
        return f'Сообщение для {self.car.brand} {self.car.model}'
