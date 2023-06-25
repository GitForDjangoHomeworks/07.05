
from django.db import models
from icecream import ic
class LatestProductsManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        length = len(qs)
        if length<6:
            return qs
        else:
            ic(qs[length-6:length])
            return qs[length-6:length]
        