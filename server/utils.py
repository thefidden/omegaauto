import os

from cars.models import CarImage


def get_image_upload_path(instance: CarImage, filename) -> str:
    ext = os.path.splitext(filename)[1].lower()
    if ext not in {'.jpg', '.jpeg', '.png'}:
        ext = '.jpg'
    return os.path.join('car-images', str(instance.car_id), f'{instance.index}{ext}')
