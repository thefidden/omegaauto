from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, AllowAny

from cars.models import CarStatus

from cars.serializers import CarStatusSerializer


class CarStatusViewSet(viewsets.ModelViewSet):
    queryset = CarStatus.objects.all()
    serializer_class = CarStatusSerializer
    filter_backends = (DjangoFilterBackend,)

    def get_permissions(self):
        admin_actions = {'create', 'update', 'partial_update', 'destroy'}

        if self.action in admin_actions:
            return [IsAdminUser()]

        return [AllowAny()]
