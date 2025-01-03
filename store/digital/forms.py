from django import forms
from django.contrib.auth.models import User
from django_svg_image_form_field import SvgAndImageFormField
from .models import Category, Profile, ShippingAddress
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm


class CategoryIconForm(forms.ModelForm):
    """Подключение возможности загрузки SVG файлов"""
    class Meta:
        model = Category
        field_classes = {
            'icon': SvgAndImageFormField
        }

        exclude = []


class LoginForm(AuthenticationForm):
    """Форма для входа в аккаунт"""
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Имя пользователя',
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Пароль',
    }))


class RegistrationForm(UserCreationForm):
    """Форма для регистрации аккаунта"""
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Имя пользователя'
    }))

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ваше имя'
    }))

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ваша фамилия'
    }))

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ваша почта'
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ваш пароль'
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Подтвердите пароль'
    }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class EditUserForm(UserChangeForm):
    """Изменение аккаунта пользователя"""
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ваше имя'
    }))

    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ваша фамилия'
    }))

    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ваша почта'
    }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class EditProfileForm(forms.ModelForm):
    """Изменение профиля пользователя"""
    avatar = forms.FileField(required=False, widget=forms.FileInput(attrs={
        'class': 'form-control',
    }))

    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Номер телефона'
    }))

    address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Адрес (ул. дом. кв.)'
    }))

    region = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Регион'
    }))

    city = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Город'
    }))

    class Meta:
        model = Profile
        fields = ('avatar', 'phone', 'address', 'region', 'city')


class ShippingAddressForm(forms.ModelForm):
    """Форма для указания адреса доставки"""
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Адрес (ул. дом. кв)'
    }))

    phone = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Номер телефона'
    }))

    region = forms.Select(attrs={
        'class': 'form-control',
    })

    city = forms.Select(attrs={
        'class': 'form-control',
    })

    class Meta:
        model = ShippingAddress
        fields = ('address', 'phone', 'region', 'city')





