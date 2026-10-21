from django.db import models


class Model(models.Model):
    objects = models.Manager()

    name = models.CharField(max_length = 50, unique = True, verbose_name = 'Название модели')
    brand = models.ForeignKey('Brand', on_delete = models.CASCADE, verbose_name = 'Марка')

    class Meta:
        verbose_name = 'Модель марки'
        verbose_name_plural = 'Модели марок'
        ordering = ('brand__name',)

    def __str__(self) -> str:
        return f'Модель {self.name} марки {self.brand.name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
