from django_filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from cars.filters import CarFilter
from cars.models import Car
from cars.serializers import CarReadSerializer, CarWriteSerializer


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.select_related('brand', 'fuel', 'gear', 'color', 'status').prefetch_related('images')
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CarFilter
    permission_classes = (IsAdminUser,)

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return CarWriteSerializer

        if self.action in ('list', 'retrieve'):
            return CarReadSerializer

        return CarReadSerializer
