from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from cars.models import CarImage
from cars.serializers import CarImageSerializer


class CarImageViewSet(viewsets.ModelViewSet):
    queryset = CarImage.objects.all()
    serializer_class = CarImageSerializer
    filter_backends = (DjangoFilterBackend, )
    permission_classes = (IsAdminUser, )
