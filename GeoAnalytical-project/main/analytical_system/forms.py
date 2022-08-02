from pyexpat import model
from attr import field
from .models import testtable
from django.forms import ModelForm, TextInput


class testtableForm(ModelForm):
    class Meta:
        model = testtable
        fields = ["title", "description"]
        widgets = {
            "title": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите поле title'
            }),
            "description": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите поле description'
            }),
        }
    