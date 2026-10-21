from django.db import models


class Brand(models.Model):
    objects = models.Manager()

    name = models.CharField(max_length = 50, unique = True, verbose_name = 'Название бренда')

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
        ordering = ('name',)

    def __str__(self) -> str:
        return f'{self.name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
