from django.db import models
from django.db import models


class Order(models.Model):
    ORDER_STATUS = (
        ('new', 'Új rendelés'),
        ('preparing', 'Készítés alatt'),
        ('ready', 'Elkészült'),
        ('delivered', 'Kiszállítva')
    )

    ORDER_TYPE = (
        ('delivery', 'Elvitelre'),
        ('dineIn', 'Helyben fogyasztás')
    )

    status = models.CharField(
        max_length=20, choices=ORDER_STATUS, default='new')
    order_type = models.CharField(max_length=20, choices=ORDER_TYPE)
    items = models.ManyToManyField('MenuItem', through='OrderItem')
    created_at = models.DateTimeField(auto_now_add=True)
