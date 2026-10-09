from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, AllowAny

from cars.models import Color
from cars.serializers import ColorSerializer


class ColorViewSet(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    filter_backends = (DjangoFilterBackend,)

    def get_permissions(self):
        admin_actions = {'create', 'update', 'partial_update', 'destroy'}

        if self.action in admin_actions:
            return (IsAdminUser(),)

        return (AllowAny(),)
