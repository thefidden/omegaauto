from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from telegram_bot.models import TelegramCarCard

from telegram_bot.serializers import TelegramCarCardReadSerializer, TelegramCarCardWriteSerializer


class TelegramCardView(viewsets.ModelViewSet):
    queryset = TelegramCarCard.objects.select_related('car')
    permission_classes = (IsAdminUser,)
    filter_backends = (DjangoFilterBackend,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TelegramCarCardReadSerializer

        if self.action in ('create', 'update', 'partial_update'):
            return TelegramCarCardWriteSerializer

        return TelegramCarCardReadSerializer
