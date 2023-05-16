from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from ribarite_na_noi.User.forms import (SignUpForm,
                                        LoginForm,
                                        )
from ribarite_na_noi.common.validators import RedirectNotLoggedUsers


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = 'login.html'
    redirect_authenticated_user = True


class UserRegisterView(RedirectNotLoggedUsers, CreateView):
    form_class = SignUpForm
    template_name = 'sign-up.html'
    success_url = reverse_lazy('welcome-page')

    user_must_be_logged = False
    no_permission_redirect_to = 'home'

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return response


class LogOut(LogoutView):
    pass
