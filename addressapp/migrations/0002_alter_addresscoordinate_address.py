# Generated by Django 3.2.15 on 2023-01-28 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addressapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addresscoordinate',
            name='address',
            field=models.CharField(max_length=255, unique=True, verbose_name='Адрес'),
        ),
    ]
