from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('telegram_bot', '0002_remove_telegramcarcard_text_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name = 'TelegramReferenceCard',
            fields = [
                ('id',
                 models.BigAutoField(auto_created = True, primary_key = True, serialize = False, verbose_name = 'ID')),
                ('text', models.TextField(verbose_name = 'Текст сообщения')),
                ('entities', models.JSONField(default = list, verbose_name = 'Сущности текста')),
            ],
            options = {
                'verbose_name': 'Эталонная карточка автомобиля',
                'verbose_name_plural': 'Эталонные карточки автомобилей',
            },
        ),
    ]
