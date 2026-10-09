from django.db import models


class TelegramReferenceCard(models.Model):
    objects = models.Manager()

    text = models.TextField(verbose_name = 'Текст сообщения')
    entities = models.JSONField(default = list, verbose_name = 'Сущности текста')

    class Meta:
        verbose_name = 'Эталонная карточка автомобиля'
        verbose_name_plural = 'Эталонные карточки автомобилей'
