from django import forms
from django.contrib.auth.forms import AuthenticationForm

from users.models import RegistrationQueries, User


class RegistrationQueryForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите email'}))
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите ваше имя'}), label='Имя')
    role = forms.TypedChoiceField(empty_value=None, choices=User.ROLE_CHOICES, required=True,
                                  widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = RegistrationQueries
        fields = ('email', 'name', 'role',)


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите ваш email'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control mb-2', 'placeholder': 'Введите пароль'
    }))

    class Meta:
        model = User
        fields = ('username', 'password',)
