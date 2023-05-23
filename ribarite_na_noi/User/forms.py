from django import forms
from django.contrib.auth.forms import (UserCreationForm,
                                       AuthenticationForm,
                                       PasswordChangeForm,
                                       UserChangeForm,
                                       )
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


class ChangePasswordForm(PasswordChangeForm):

    old_password = forms.CharField(
        label="",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autofocus": True,
                   "class": "form-control",
                   "placeholder": "Current password",
                   }
        ),
    )

    new_password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={"placeholder": "New password",
                   "class": "form-control",
                   }
        ),
        strip=False,

    )
    new_password2 = forms.CharField(
        label="",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"placeholder": "New password confirmation",
                   "class": "form-control",
                   }
        ),
    )


class ChangeUsernameForm(forms.ModelForm):
    USERNAME_MAX_LENGTH = 20
    USERNAME_MIN_LENGTH = 3

    old_username = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'old-username',
                'class': 'form-control',
                'autofocus': True,
            }
        ),
        label="",
    )

    new_username = forms.CharField(
        max_length=USERNAME_MAX_LENGTH,
        required=True,
        validators=(
            validate_name,
            MinLengthValidator(USERNAME_MIN_LENGTH),
        ),
        widget=forms.TextInput(
            attrs={
                'placeholder': 'new-username',
                'class': 'form-control',
            }
        ),
        label="",
    )

    class Meta:
        model = User
        fields = ("old_username", "new_username")

    def clean(self):
        cleaned_data = super().clean()
        old_username = cleaned_data.get('old_username')
        new_username = cleaned_data.get('new_username')

        old_user = User.objects.filter(username=old_username)
        new_user = User.objects.filter(username=new_username)

        if not old_user:
            raise forms.ValidationError("Invalid old username")

        if old_username == new_username:
            raise forms.ValidationError("New username cannot be same as old username")

        if new_user.exists():
            raise forms.ValidationError("Username already exists")

    def save(self, commit=True):
        user = User.objects.filter(username=self.cleaned_data.get("old_username")).get()
        user.username = self.cleaned_data.get("new_username")
        user.save()
