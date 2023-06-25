from statistics import quantiles
from django import forms

class CartAddProductForm(forms.Form):
    quantity = forms.CharField(label='Количество')
    update = forms.BooleanField(required=False, initial=False, widget = forms.HiddenInput)
    page_id = forms.IntegerField(),

    class Meta:
        fields = ('quantity', 'update')
        widgets = {
            'quantity': forms.TextInput(
                attrs={'class': 'product_quantity js_numder',
                'value' : 1}),

      

        'update' : forms.HiddenInput(),
        'page_id' : forms.HiddenInput(),
        }