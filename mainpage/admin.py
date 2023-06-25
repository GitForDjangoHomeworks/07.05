from django.contrib import admin
from .models import (
    MainPageServices,
    FooterAbout,
    Social,
    Menu,
    NavMenu,
    Brands
)
# Register your models here.

admin.site.register(MainPageServices)
admin.site.register(FooterAbout)
admin.site.register(Social)
admin.site.register(Menu)
admin.site.register(NavMenu)
admin.site.register(Brands)