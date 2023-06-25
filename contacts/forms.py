from django import forms
from .models import ContactPageForm
from .validators import validate_phone_number
from django.core.exceptions import ValidationError

from captcha.fields import CaptchaField
from icecream import ic
from django.utils.translation import gettext_lazy as _

class ContactFormDB(forms.Form):
    number = forms.CharField(label='Номер телефона')
    subject = forms.CharField(max_length=100)
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    message = forms.CharField()
    captcha = CaptchaField(label="Решите пример")

    class Meta:
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Предмет сообщения'
            }),
            'name': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Имя'
            }),
        
            'email': forms.EmailInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Email'
            }),
            'message': forms.Textarea(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Сообщение'
            }), 
        }
    def clean(self):
        cleaned_data = super().clean()
        
        errors = {}
        value = cleaned_data.get('number')
        for i in value:
            if i not in ('1234567890'):
                errors['number'] = ValidationError(_('Phone number must have only digits'))
                break
        
        ic(errors)
        if errors:
            raise ValidationError(errors)
        