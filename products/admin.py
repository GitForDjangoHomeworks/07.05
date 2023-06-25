
from django.contrib import admin
from .models import SingleProduct, Category, ProductImage
# Register your models here.

class SingleProductAdmin(admin.ModelAdmin):
    list_display = ('pk','name','category','end_price','number_products', 'in_store', 'content')
    list_display_links = ('pk',)
    list_editable = ('name','in_store', 'category',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk','name','show_description')
    list_display_links = ('pk',)
    list_editable = ('name',)
    
    def show_description(self,obj):
        return f'{obj.description[:40]}'

admin.site.register(SingleProduct, SingleProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductImage)
