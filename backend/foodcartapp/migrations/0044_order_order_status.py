# Generated by Django 3.2.15 on 2023-01-02 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0043_rename_orderproductnew_orderproduct'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('AC', 'Принят'), ('AS', 'Сборка'), ('DL', 'Доставка'), ('FN', 'Завершен')], default='AC', max_length=2, verbose_name='Статус заказа'),
        ),
    ]