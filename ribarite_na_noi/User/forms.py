from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator

from ribarite_na_noi.common.validators import validate_name


class LoginForm(AuthenticationForm):

    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Username',
                'autofocus': True,
            }
        ),
        label="",
    )
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={
             'class': 'form-control',
             'placeholder': 'Password',
             }
        ),
        label="",
    )


class SignUpForm(UserCreationForm):
    USERNAME_MAX_LENGTH = 20
    USERNAME_MIN_LENGTH = 3

    PASSWORD_MAX_LENGTH = 15
    PASSWORD_MIN_LENGTH = 4

    username = forms.CharField(
        max_length=USERNAME_MAX_LENGTH,
        required=True,
        validators=(
            validate_name,
            MinLengthValidator(USERNAME_MIN_LENGTH),
        ),
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username',
                'class': 'form-control',
                'autofocus': True,
            }
        ),
        label="",
    )

    password1 = forms.CharField(
        max_length=PASSWORD_MAX_LENGTH,
        required=True,
        validators=(
            MinLengthValidator(PASSWORD_MIN_LENGTH),
        ),
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
                'class': 'form-control',
            }
        ),
        label="",
    )

    password2 = forms.CharField(
        max_length=PASSWORD_MAX_LENGTH,
        required=True,
        validators=(
            MinLengthValidator(PASSWORD_MIN_LENGTH),
        ),
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirm Password',
                'class': 'form-control',
            }
        ),
        label="",
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')