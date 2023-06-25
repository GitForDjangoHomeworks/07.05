from django.db import models

# Create your models here.

class ContactPage(models.Model):
    adress = models.CharField(verbose_name='Адрес', max_length=50, blank=True)
    phone = models.CharField(verbose_name='Телефон', max_length=50, blank=True)
    email = models.EmailField(verbose_name='Email')
    website = models.CharField(verbose_name='Веб Сайт', max_length=50, blank=True)

    class Meta:
        verbose_name = 'Контакты'
        verbose_name_plural = 'Контакты'

    def __str__(self) -> str:
        return f'{self.adress}'


class ContactPageForm(models.Model):
    name = models.CharField(verbose_name='Полное имя', max_length=50)
    email = models.EmailField(verbose_name='Email')
    subject = models.CharField(verbose_name='Тема', max_length=100)
    message = models.TextField(verbose_name='Текст сообщения')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self) -> str:
        return f'{self.subject}'