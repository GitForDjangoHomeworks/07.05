from django.db import models
from django.contrib.auth.models import User, Group
# Create your models here.

class CustomUser(User):
    pass

class CustomGroup(Group):
    is_admin = models.BooleanField(default=False)
    