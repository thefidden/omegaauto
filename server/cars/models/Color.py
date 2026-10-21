from django.db import models


class Color(models.Model):
    objects = models.Manager()

    name = models.CharField(max_length = 50, unique = True, verbose_name = 'Цвет')

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'
        ordering = ('name',)

    def __str__(self) -> str:
        return f'{self.name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
