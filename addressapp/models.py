from django.db import models
from django.utils import timezone


class AddressCoordinate(models.Model):
    """Модель адресов и их координат"""
    address = models.TextField(unique=True, verbose_name='Адрес')
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')

    request_date = models.DateTimeField(default=timezone.now, verbose_name='Координаты обновлены', db_index=True)

    class Meta:
        verbose_name = 'адрес'
        verbose_name_plural = 'адреса'
