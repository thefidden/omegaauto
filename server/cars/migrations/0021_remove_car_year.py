from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0020_alter_car_release_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name = 'car',
            options = {
                'ordering': ('brand', 'model', 'release_date', 'mileage', 'updated_at'),
                'verbose_name': 'Автомобиль',
                'verbose_name_plural': 'Автомобили',
            },
        ),
        migrations.RemoveField(
            model_name = 'car',
            name = 'year',
        ),
    ]
