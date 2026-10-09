from django.contrib import admin

from telegram_bot.models import TelegramCarCard


@admin.register(TelegramCarCard)
class TelegramCarCardAdmin(admin.ModelAdmin):
    list_display = ('car', 'link', 'created_at')
    list_filter = ('car',)
    ordering = ('-created_at', 'car')
