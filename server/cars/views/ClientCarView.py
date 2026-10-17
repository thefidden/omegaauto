from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from cars.filters import CarFilter
from cars.models import Car
from cars.paginations import CarPagination
from cars.serializers import ClientCarSerializer


class ClientCarViewSet(viewsets.ModelViewSet):
    queryset = CarFilter(
        data = { 'only_available': True },
        queryset = (
            Car
            .objects
            .select_related('brand', 'fuel', 'gear', 'color', 'status')
            .prefetch_related('images')
            .order_by('-created_at')
        )
    ).qs

    filter_backends = (DjangoFilterBackend,)
    filterset_class = CarFilter

    serializer_class = ClientCarSerializer
    pagination_class = CarPagination

    permission_classes = (AllowAny,)
    http_method_names = ('get',)
