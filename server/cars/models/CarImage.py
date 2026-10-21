from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
import uuid

from cars.models.Car import Car
from utils import get_image_upload_path


class CarImage(models.Model):
    objects = models.Manager()

    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    car: Car = models.ForeignKey(Car, related_name = 'images', on_delete = models.CASCADE, verbose_name = 'Автомобиль')
    image = models.ImageField(upload_to = get_image_upload_path, verbose_name = 'Изображение', null = True,
                              default = None, blank = True)
    public = models.BooleanField(default = True, verbose_name = 'Публичное')
    index = models.PositiveSmallIntegerField(verbose_name = 'Порядковый номер')

    class Meta:
        verbose_name = 'Изображение автомобиля'
        verbose_name_plural = 'Изображения автомобилей'
        ordering = ('car', 'index')

    def __str__(self):
        return f'Изображение для {self.car.brand} {self.car.model}'


@receiver(post_delete, sender = CarImage)
def delete_car_image_file(sender, instance: CarImage, **kwargs):
    if instance.image:
        instance.image.delete(save = False)
