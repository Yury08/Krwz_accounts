from django import forms
from django.contrib.auth.models import User
from .models import Profile

# Регистрация
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='подтвердите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']

# Профиль
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('photo', )

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
