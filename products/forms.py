
from django import forms

from django.core.exceptions import ValidationError
from .models import SingleProduct, ProductImage, Category

from django.core import validators

class ProductForm(forms.ModelForm):
    error_css_class = 'error'

    document = forms.FileField(
        label = 'Сопроводительный документ',
        validators=[validators.FileExtensionValidator(
            allowed_extensions =(
                'doc',
                'docx',
                'xls',
                'xlsx',
                'pdf'
            )
        )
            ],
        error_messages={'invalid_extension' : 'Этот формат не поддерживается'}
    )
    class Meta:
        model = SingleProduct
        fields = '__all__'


    def clean(self):
        super().clean()
        errors = {}

        if self.cleaned_data.get('initial_price') < 0:
            # errors['initial_price'] = ValidationError('Цена не может быть меньше нуля')
            self.add_error('initial_price', ValidationError('Price should be more than 0'))
        # if errors:
        #     raise ValidationError(errors)
    
class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = '__all__'

    def clean(self):
        erorrs = {}

        cleaned_data = super().clean()
        if len(cleaned_data['description'])>50:
            erorrs['description'] = ValidationError('Длина описания не может превышать 50 символов')
            # self.add_error('description', ValidationError('Длина описания не может превышать 50 символов'))

        if erorrs:
            raise ValidationError(erorrs)

class CategoryDetailForm(forms.ModelForm):
    error_css_class = 'error'
    document = forms.FileField( label='Necessary Document',
                                validators=[validators.FileExtensionValidator(allowed_extensions=[
                                   'xlsx',
                                   'pdf']
                                  
                               )],
                                error_messages={'invalid_extension':'Этот файл не поддерживается'}
                               )
    class Meta:
        model = Category
        fields = '__all__'