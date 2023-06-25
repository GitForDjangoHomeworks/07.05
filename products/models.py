from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import LatestProductsManager
from precise_bbcode.fields import BBCodeTextField
class SingleProduct(models.Model):
    name = models.CharField(verbose_name='Название', max_length=200)
    description = models.TextField(verbose_name='Описание',blank=True)
    category = models.ForeignKey(verbose_name='Категория товара', to='Category', on_delete=models.CASCADE, default=1, related_name='products')
    initial_price = models.BigIntegerField(verbose_name='Цена')
    discount = models.PositiveIntegerField(verbose_name='Процент скидки',blank=True)
    end_price = models.PositiveBigIntegerField(verbose_name='Цена с учетом скидки',editable=False)
    number_products = models.PositiveBigIntegerField(verbose_name='Количество товаров', blank=True, null=True)
    in_store = models.BooleanField(verbose_name='Доступен', default=True)
    images = models.ManyToManyField(to='ProductImage', verbose_name='Картины',blank =True)   
    order = models.SmallIntegerField(default=0, db_index=True)
    content = BBCodeTextField(verbose_name=_('Содержание'), blank = True, null=True)
    document = models.FileField(    verbose_name=_('Документы'),
                                    upload_to='documents/produsts/%Y/%m/%d/',    blank=True,
                                    null=True)

    # CUSTOM MANAGERS
    objects = models.Manager()
    latest_products = LatestProductsManager()
    
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['order', 'name']

    def __str__(self):
        return f'{self.category}-{self.name}'

    def save(self,*args, **kwargs):
        if self.discount:
            self.end_price = self.initial_price * (100-self.discount) / 100
        else:
            self.end_price = self.initial_price
        super().save(*args, **kwargs)

class Category(models.Model):
    name = models.CharField(verbose_name ='Название категории', max_length =50, blank=True)
    description = models.TextField(verbose_name ='Описание', blank=True)
    image = models.ImageField(verbose_name='Картина',upload_to = 'category')
    document = models.FileField(    verbose_name=_('Документы'),
                                    upload_to='documents/categories/%Y/%m/%d/',    blank=True,
                                    null=True)


    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']
    def __str__(self):
        return f'{self.name}'


class ProductImage(models.Model):
    image = models.ImageField(verbose_name='Картина', upload_to ='products/%d%m%Y', blank = True)
    description = models.CharField(verbose_name='Описание', max_length=200)
    order = models.PositiveSmallIntegerField(default=0, db_index=True)

    class Meta:
        verbose_name = 'Картина Продукта'
        verbose_name_plural = 'Картины продукта'

    def __str__(self):
        return f'{self.description}'
