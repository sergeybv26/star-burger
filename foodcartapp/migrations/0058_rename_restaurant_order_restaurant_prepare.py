# Generated by Django 3.2.15 on 2023-02-21 06:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0057_rename_cooks_restaurant_order_restaurant'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='restaurant',
            new_name='restaurant_prepare',
        ),
    ]
