from django.db import models


class CarStatus(models.Model):
    objects = models.Manager()

    name = models.CharField(max_length = 50, unique = True, verbose_name = 'Статус')

    class Meta:
        verbose_name = 'Статус автомобиля'
        verbose_name_plural = 'Статусы автомобилей'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
