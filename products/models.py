from django.contrib.auth import get_user_model
from django.db import models


class Product(models.Model):
    """
    Модель для хранения информации о товаре.
    """

    SALE_STATUS = [
        (True, 'В продаже'),
        (False, 'Снят с продажи')
    ]

    product_title = models.CharField(max_length=255, verbose_name='Наименование товара')
    seller = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name='seller', verbose_name='Продавец')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена товара')
    is_active_sale = models.BooleanField(default=True, choices=SALE_STATUS, verbose_name='Статус товара')

    objects = models.Manager

    @property
    def shop_name(self):
        return self.seller.shop_name

    def __str__(self):
        return f'{self.product_title} {self.shop_name} {self.seller}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
