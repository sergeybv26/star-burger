# Generated by Django 3.2.15 on 2023-01-07 17:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AddressCoordinate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField(unique=True, verbose_name='Адрес')),
                ('lat', models.FloatField(verbose_name='Широта')),
                ('lon', models.FloatField(verbose_name='Долгота')),
                ('request_date', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='Координаты обновлены')),
            ],
            options={
                'verbose_name': 'адрес',
                'verbose_name_plural': 'адреса',
            },
        ),
    ]
