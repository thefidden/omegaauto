from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.serializers import ModelSerializer

from cars.filters import ModelFilter
from cars.models import Model


class ModelViewSet(viewsets.ModelViewSet):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer

    filterset_class = ModelFilter
    filter_backends = (DjangoFilterBackend,)

    def get_permissions(self):
        admin_actions = {'create', 'update', 'partial_update', 'destroy'}

        if self.action in admin_actions:
            return (IsAdminUser(),)

        return (AllowAny(),)
