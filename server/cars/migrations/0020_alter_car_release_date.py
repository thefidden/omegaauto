# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0019_car_release_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name = 'car',
            name = 'release_date',
            field = models.DateTimeField(verbose_name = 'Дата выпуска'),
        ),
    ]
