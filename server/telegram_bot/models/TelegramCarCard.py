from django.db import models


class TelegramMessage(models.Model):
    objects = models.Manager()

    text = models.TextField(verbose_name = 'Текст сообщения')
    link = models.CharField(max_length = 50, verbose_name = 'Ссылка на сообщение', unique = True)

    created_at = models.DateTimeField(auto_now_add = True, verbose_name = 'Дата создания')
    updated_at = models.DateTimeField(auto_now = True, verbose_name = 'Дата обновления')

    class Meta:
        verbose_name = 'Сообщение Telegram'
        verbose_name_plural = 'Сообщения Telegram'

    def __str__(self):
        return f'Сообщение {self.link}'
