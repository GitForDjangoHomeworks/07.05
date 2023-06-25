from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Customer(User):
    second_phone = models.CharField(verbose_name='Второй телефон', max_length=14)
    telegram = models.CharField(verbose_name='Телеграм ник', max_length=50)
    

