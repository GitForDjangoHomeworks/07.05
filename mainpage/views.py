
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.forms import modelformset_factory
from django.forms.formsets import ORDERING_FIELD_NAME
from django.views.generic import ListView
from products.models import SingleProduct, Category
from products.forms import ProductForm, ProductImageForm
# Create your views here.

class MainPageTemplateView(ListView):
    template_name = 'mainpage/index.html'
    model = Category
    context_object_name = 'categories'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_products'] = SingleProduct.latest_products.all()
        '''
            Здесь  я использую prefetch_related  к полю images так как там ManyToMany relationship
            prefetch_related нужен чтобы уменьшить колво запросов в базу данных
            а этот метод помогает сразу брать поле images при первом запросе к продукты
        '''
        return context


        