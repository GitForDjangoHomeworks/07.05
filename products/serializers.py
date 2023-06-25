from .models import SingleProduct, Category
from rest_framework import serializers
class ProductNameAmmountPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SingleProduct
        fields = (
            'name',
            'initial_price',
            'number_products',
            'discount',
        )

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('pk', 'name')