from django.shortcuts import render, redirect, get_object_or_404
from precise_bbcode.bbcode import get_parser
from pathlib import Path
from django.conf import settings

from django.views.generic.base import TemplateView
from django.forms import modelformset_factory, inlineformset_factory
from django.forms.formsets import ORDERING_FIELD_NAME
from django.views.generic import ListView, DetailView

#REST IMPORTS
from rest_framework import generics, viewsets
from .serializers import ProductNameAmmountPriceSerializer, CategorySerializer

from django.db import transaction

from products.models import SingleProduct, Category, ProductImage
from products.forms import ProductForm, ProductImageForm, CategoryDetailForm
from pages.forms import AddFileForm
from icecream import ic
# Create your views here.

class SingleProductPageDetailView(DetailView):
    template_name = 'products/single_product.html'
    context_object_name = 'product'
    model = SingleProduct   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parser = get_parser()
        context['from_view'] = parser.render('[b]Здравствуйте, люди [u]дорогие![/u][/b]')
        return context


class ProductDetailEditView(DetailView):
    template_name = "products/single_product_edit.html"
    model = SingleProduct
    context_object_name = "product"
    form_class = ProductForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ProductForm(instance=self.get_object())
        return context

    def post(self, request, *args, **kwargs):
        form = ProductForm(request.POST, request.FILES, instance=self.get_object())
        if form.is_valid():
            return self.form_valid(form)

        return render(request, "products/single_product_edit.html", {"form": form})

    def form_valid(self, form):
        product = form.save(commit=False)
        ic('goos')
        product.save()
        return redirect("products:show_single_product_page", pk=product.pk)


class CategoryDetailView(DetailView):
    template_name = 'products/category_view.html'
    context_object_name = 'category'
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = kwargs['object']
        ic(kwargs)
        parser = get_parser()
        context['from_view'] = parser.render(f'[quote][b]Этот каталог {category.name}  [/b][/quote]')
        return context

class CategoryDetailEditView(DetailView):
    context_object_name = 'category'
    model = Category
    template_name = 'products/category_detail_edit_view.html'
    form_class = CategoryDetailForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CategoryDetailForm(instance=self.get_object())
        return context

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST, request.FILES,
                               instance=self.get_object())
        if form.is_valid():

            return self.form_valid(form)

        return render(request, template_name=self.template_name, context={'form': form})

    def form_valid(self, form):
        category = form.save(commit=False)
        category.save()
        return redirect('products:category_view', pk=category.pk)

def category_add_file(request, pk):
    category = Category.objects.get(pk=pk)
    if request.method == 'POST':
        form = AddFileForm(request.POST, request.FILES)
        if form.is_valid():
            ic(form.cleaned_data)
            uploaded_file = request.FILES['file']
            filename = f'{uploaded_file.name}'
            file_with_path = Path(settings.CATEGORIES_DOCUMENTS_ROOT, filename)
            category.document = uploaded_file
            category.save()
            with open (file_with_path, 'wb') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            redirect ('mainpage:show_mainpage')
    else:
        form = AddFileForm()
    context = {'form': form}
    template_name = 'products/categories_file_add.html'
    return render(request, template_name, context=context)
                
#BULK EDITS WITH FORMSETS
def products_bulk_edit(request):
    ProductFormSet = modelformset_factory(
        SingleProduct, form=ProductForm, fields=('name', 'description', 'in_store', 'initial_price'),
         extra=1, can_delete=True, can_order=True
    )
    template_name = 'products/product_bulk_edit.html'
    context = {}

    if request.method == 'POST':
        formset = ProductFormSet(request.POST)

        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    save_point = transaction.savepoint()
                    product = form.save(commit=False)
                    product.order = form.cleaned_data[ORDERING_FIELD_NAME]
                    try:

                        product.save()
                        transaction.savepoint_commit(save_point)
                    except:
                        transaction.rollback()
                    transaction.commit()
            return redirect('products:products_bulk_edit')
    else:
        formset = ProductFormSet(queryset=SingleProduct.objects.prefetch_related('images'))
        '''
            Здесь  я использую prefetch_related  к полю images так как там ManyToMany relationship
            prefetch_related нужен чтобы уменьшить колво запросов в базу данных
            а этот метод помогает сразу брать поле images при первом запросе к продукты
        '''
    context['product_form_set'] = formset
    return render(request, template_name, context)


class ProductImageBulkEditListView(TemplateView):
    template_name = 'products/product_image_bulk_edit.html'
    ProductImgaeFormset = modelformset_factory(ProductImage, form=ProductImageForm, 
                        fields=('description', 'image'), can_delete=True, can_order=True, extra=1)
    
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     queryset['product_images'] = ProductImage.objects.all()
    #     return queryset
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_image_formset'] = self.ProductImgaeFormset(queryset=ProductImage.objects.all())
        return context
    def post(self, request, *args, **kwargs):
        ic('post')
        formset = self.ProductImgaeFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    product_image = form.save(commit=False)
                    product_image.order = form.cleaned_data[ORDERING_FIELD_NAME]
                    product_image.save()
                return redirect('products:product_image_bulk_edit')
        else:
            self.get_context_data()['product_image_formset'] = formset
            ic(formset.errors)
            return render(request, self.template_name, self.get_context_data())



        
#API
class ProductNameAmmountPriceAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SingleProduct.objects.all()
    serializer_class = ProductNameAmmountPriceSerializer

    def get(self, request, *args, **kwargs):
        product = get_object_or_404(SingleProduct, pk=kwargs['pk'])
        product.save()

    
        return self.retrieve(request, *args, **kwargs)

class CategoryAPIView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    