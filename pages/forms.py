from django import forms

class AddFileForm(forms.Form):
    file = forms.FileField(label='File',)