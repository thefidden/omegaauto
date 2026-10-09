import os

from cars.models import CarImage


def get_image_upload_path(instance: CarImage, filename) -> str:
    return os.path.join('car-images', f'{instance.car.id}-{instance.id}.jpg')