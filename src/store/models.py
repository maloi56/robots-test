from django.core.validators import MinValueValidator
from django.db import models


class Warehouse(models.Model):
    model = models.CharField(verbose_name='Модель', max_length=2, blank=False, null=False)
    version = models.CharField(verbose_name='Версия', max_length=2, blank=False, null=False)
    quantity = models.PositiveIntegerField(verbose_name='Количество', default=1, blank=False, null=False)

    def __str__(self):
        return f'{self.model}:{self.version}'

    class Meta:
        verbose_name = "робот на складе"
        verbose_name_plural = "роботы на складе"
        unique_together = ("model", "version")


class Product(models.Model):
    robot = models.OneToOneField(verbose_name='Робот',
                                 to=Warehouse, related_name='product', on_delete=models.PROTECT)
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    price = models.DecimalField(verbose_name='Цена', max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    image = models.ImageField(verbose_name='Изображение', upload_to='products_images', null=True, blank=True)

    def __str__(self):
        return f'{self.robot}'

    class Meta:
        verbose_name = "робот на продаже"
        verbose_name_plural = "роботы на продаже"
