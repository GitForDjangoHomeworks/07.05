from django import forms
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField
from .models import Order

class OrderCreateForm(forms.ModelForm):
    captcha = CaptchaField(label="Введите картинку")
    class Meta:
        model = Order
        fields = (
            'first_name', 'last_name', 
            'email', 'phone', 'address',
            'postal_code', 'city'
        )
        