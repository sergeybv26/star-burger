# Generated by Django 3.2.15 on 2023-02-17 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0056_auto_20230217_1550'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='cooks_restaurant',
            new_name='restaurant',
        ),
    ]