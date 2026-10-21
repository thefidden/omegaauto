from django.db import models


class Fuel(models.Model):
    objects = models.Manager()

    name = models.CharField(max_length = 50, unique = True, verbose_name = 'Вид топлива')

    class Meta:
        verbose_name = 'Вид топлива'
        verbose_name_plural = 'Виды топлива'
        ordering = ('name',)

    def __str__(self) -> str:
        return f'{self.name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
