from django.contrib.auth import (authenticate,
                                 login,
                                 )
from django.contrib.auth.models import User
from django.contrib.auth.views import (LoginView,
                                       LogoutView,
                                       PasswordChangeView,
                                       PasswordChangeDoneView,
                                       )
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView,
                                  DetailView,
                                  FormView,
                                  TemplateView,
                                  DeleteView,
                                  )

from ribarite_na_noi.Braids.models import Braid
from ribarite_na_noi.Chepareta.models import Chepare
from ribarite_na_noi.Leads.models import Lead
from ribarite_na_noi.Reels.models import Reel
from ribarite_na_noi.Rods.models import Rod
from ribarite_na_noi.User.forms import (SignUpForm,
                                        LoginForm,
                                        ChangePasswordForm,
                                        ChangeUsernameForm,
                                        )
from ribarite_na_noi.common.validators import (RedirectNotLoggedUsers,
                                               RedirectLoggedUsersUrlTypers,
                                               )


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


class ProfileView(RedirectLoggedUsersUrlTypers, DetailView):
    model = User
    template_name = 'profile.html'

    user_must_be_logged = True
    no_permission_redirect_to = 'login'

    def get_number_of_created_models(self):
        result = {}

        all_models = (
            (Rod, "Въдици"),
            (Reel, "Макари"),
            (Braid, "Влакна"),
            (Chepare, "Чепарета"),
            (Lead, "Олова")
        )
        user = self.get_object()
        for model, bg_name in all_models:
            result[bg_name] = model.objects.filter(created_by=user.pk).count()

        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_posts'] = self.get_number_of_created_models()
        context['created_items'] = sum(context['all_posts'].values())

        return context


class ChangePassword(RedirectNotLoggedUsers, PasswordChangeView):
    form_class = ChangePasswordForm
    success_url = reverse_lazy("successful_password_change")
    template_name = 'change-password.html'

    no_permission_redirect_to = 'login'

    def get(self, request, *args, **kwargs):

        if kwargs['pk'] != self.request.user.pk:
            return redirect('profile', pk=self.request.user.pk)

        return super().get(request, *args, **kwargs)


class SuccessPasswordChange(RedirectNotLoggedUsers, PasswordChangeDoneView):
    template_name = 'successful-page.html'
    no_permission_redirect_to = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['success_message'] = "Успешно сменихте паролата си !"

        return context


class ChangeUsername(RedirectNotLoggedUsers, FormView):
    form_class = ChangeUsernameForm
    template_name = 'change-username.html'
    success_url = reverse_lazy('successful_username_change')

    no_permission_redirect_to = 'login'

    def get(self, request, *args, **kwargs):
        if kwargs['pk'] != self.request.user.pk:
            return redirect('profile', pk=self.request.user.pk)

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        if self.request.user.username != form.cleaned_data.get("old_username"):
            return redirect('profile', pk=self.request.user.pk)

        form.save()
        return super().form_valid(form)


class SuccessUsernameChange(RedirectNotLoggedUsers, TemplateView):
    template_name = 'successful-page.html'
    no_permission_redirect_to = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['success_message'] = f"Успешно сменихте потребителското си име на {self.request.user.username} !"

        return context


class DeleteUser(ProfileView, RedirectNotLoggedUsers, DeleteView):
    model = User
    template_name = 'delete-user.html'
    no_permission_redirect_to = 'login'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delete_user_msg'] = "Наистина ли искаш да си изтриеш профила ?"

        return context



