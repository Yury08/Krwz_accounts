from django import forms
from django.forms import TextInput
from django.forms.models import inlineformset_factory
from .models import (
    ImageGallery,
    Product,
    Orders,
    Comments
)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('name', 'text')


class OrderForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': TextInput(attrs={'placeholder': 'Имя'}),
            'last_name': TextInput(attrs={'placeholder': 'Фамилия'}),
            'email': TextInput(attrs={'placeholder': 'Почта'})}


ImageFormSet = inlineformset_factory(Product,
                                     ImageGallery,
                                     fields=['title', 'image'],
                                     extra=3,
                                     can_delete=True)

