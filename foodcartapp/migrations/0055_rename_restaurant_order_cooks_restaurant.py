# Generated by Django 3.2.15 on 2023-01-28 10:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0054_alter_order_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='restaurant',
            new_name='cooks_restaurant',
        ),
    ]
