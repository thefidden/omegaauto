import uuid

from django.db import models

class Car(models.Model):
    objects = models.Manager()

    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

    model = models.CharField(max_length = 50, verbose_name = 'Модель')
    year = models.PositiveSmallIntegerField(verbose_name = 'Год выпуска')
    mileage = models.PositiveIntegerField(verbose_name = 'Пробег')
    power = models.PositiveIntegerField(verbose_name = 'Мощность, л.с.')
    displacement = models.DecimalField(max_digits = 2, decimal_places = 1, verbose_name = 'Объем двигателя')
    vin = models.CharField(max_length = 20, verbose_name = 'VIN-номер', blank = True)
    price = models.PositiveIntegerField(verbose_name = 'Стоимость')

    brand = models.ForeignKey('Brand', on_delete = models.PROTECT, related_name = 'cars', verbose_name = 'Марка')
    fuel = models.ForeignKey('Fuel', on_delete = models.PROTECT, related_name = 'cars', verbose_name = 'Топливо')
    gear = models.ForeignKey('Gear', on_delete = models.PROTECT, related_name = 'cars', verbose_name = 'Трансмиссия')
    color = models.ForeignKey('Color', on_delete = models.PROTECT, related_name = 'cars', verbose_name = 'Цвет')
    status = models.ForeignKey('CarStatus', on_delete = models.PROTECT, related_name = 'cars', verbose_name = 'Статус')

    created_at = models.DateTimeField(auto_now_add = True, verbose_name = 'Дата создания')
    updated_at = models.DateTimeField(auto_now = True, verbose_name = 'Дата изменения')

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'
        ordering = ('brand', 'model', 'year', 'mileage', 'updated_at')

    def __str__(self):
        return f'{self.brand} {self.model}'
