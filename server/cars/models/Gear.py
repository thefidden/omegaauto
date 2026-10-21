from django.db import models


class Gear(models.Model):
    objects = models.Manager()

    name = models.CharField(max_length = 50, unique = True, verbose_name = 'Коробка передач')

    class Meta:
        verbose_name = 'Коробка передач'
        verbose_name_plural = 'Коробки передач'
        ordering = ('name',)

    def __str__(self) -> str:
        return f'{self.name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
