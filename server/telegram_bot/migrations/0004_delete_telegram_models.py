from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('telegram_bot', '0003_telegramreferencecard'),
    ]

    operations = [
        migrations.DeleteModel(
            name = 'TelegramCarCard',
        ),
        migrations.DeleteModel(
            name = 'TelegramReferenceCard',
        ),
    ]
