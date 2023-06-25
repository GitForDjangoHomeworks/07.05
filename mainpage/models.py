from distutils.command.upload import upload
from multiprocessing.spawn import import_main_path
from tabnanny import verbose
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from django.conf import settings

from easy_thumbnails.fields import ThumbnailerImageField
# Create your models here.
            #FOOTER
class PageBlock(models.Model):
    title = models.CharField(_('Заголовок'), max_length=250, blank=True)
    icon_class = models.CharField(_('Иконка'), max_length=255, blank=True)
    text = models.TextField(_('Текст'), blank=True)
    url = models.URLField(_('Ссылка'), blank=True)

    class Meta:
        abstract = True

class MainPageServices(PageBlock):
    class Meta:
        verbose_name = _('Услуга')
        verbose_name_plural = _("Услуги")

        ordering = ('title',)
    def __str__(self):
        return f"{self.title}"

class FooterAbout(models.Model):
    title = models.CharField(
        verbose_name=_('Заголовок о нас'), max_length=250, blank=True
    )
    text = models.TextField(verbose_name=_('Текст о нас'), blank=True)
    social = models.ManyToManyField(to='Social', verbose_name=_('Соц сети'), blank=True)
    menu = models.ManyToManyField(to='Menu', verbose_name=_('Меню'), blank=True)

class Social(PageBlock):
    class Meta:
        verbose_name =_('Социальная сеть')
        verbose_name_plural = _('Социальные сети')
    def __str__(self):
        return f'{self.title}'
class Menu(PageBlock):
    class Meta:
        verbose_name = _('Меню')
        verbose_name_plural = _('Меню')

    def __str__(self):
        return f'{self.title}'

#NAV

class NavMenu(models.Model):
    title = models.CharField(verbose_name=_('Заголовок'), max_length=100 )
    url = models.CharField(verbose_name='Ссылка на страницу', max_length=100)

    class Meta:
        verbose_name = _('Меню Навигации')
        verbose_name_plural = _('Меню Навигации')
        ordering = ['title', ]

        

#BRANDS
class Brands(PageBlock):
    thumb_path = settings.THUMBNAIL_BASEDIR + "/%Y/%m/%d"
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to = "%Y/%m/%d",
        blank = True,
    )
    image_thumbnail = ThumbnailerImageField(
        resize_source = {'size': (800,800), 'crop':'smart'}, upload_to=thumb_path,
        blank=True
    )
    class Meta:
        verbose_name = _('Бренд')
        verbose_name_plural = _('Бренды')
    
    def __str__(self):
        return f'{self.title}'