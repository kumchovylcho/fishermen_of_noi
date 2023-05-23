from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (ListView,
                                  CreateView,
                                  DetailView,
                                  UpdateView,
                                  DeleteView,
                                  )

from ribarite_na_noi.Chepareta.forms import (SortCheparetaForm,
                                             CreateChepareForm,
                                             FilterCheparetaForm,
                                             )
from ribarite_na_noi.Chepareta.models import Chepare
from ribarite_na_noi.common.validators import (RedirectNotLoggedUsers,
                                               RedirectLoggedUsersUrlTypers,
                                               )


class DisplayCheparetaView(ListView):
    template_name = 'display-chepareta.html'
    model = Chepare

    @property
    def get_filter_options(self):
        return {"type": Chepare.TYPE_CHOICES[1:-1],
                "number_of_hooks": Chepare.HOOK_COUNT_CHOICES[1:-1],
                "hook_number": Chepare.HOOK_NUMBER_CHOICES[1:-1],
                "color": Chepare.COLOR_CHOICES[1:-1],
                }

    def get_filter_atr(self, user_filter):
        for key, value in self.get_filter_options.items():
            for option, _ in value:
                if user_filter == option:
                    return key

        return False

    def get_queryset(self):
        queryset = super().get_queryset()

        user_filter = self.request.GET.get('filter_by')
        ordering = self.request.GET.get('sort_by', 'hook_number')

        if "clear_filters" in self.request.GET:
            self.request.GET = self.request.GET.copy()
            self.request.GET.pop("filter_by")
            self.request.GET.pop("clear_filters")

        elif "clear_filters" not in self.request.GET:
            filter_atr = self.get_filter_atr(user_filter)
            if filter_atr:
                queryset = queryset.filter(**{filter_atr: user_filter})

        queryset = queryset.order_by(ordering)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort_form'] = SortCheparetaForm(self.request.GET)
        context['filters'] = FilterCheparetaForm(self.request.GET)
        context['all_chepareta'] = Chepare.objects.all()

        return context


class CreateChepareView(RedirectNotLoggedUsers, CreateView):
    form_class = CreateChepareForm
    template_name = 'create-chepare.html'
    success_url = reverse_lazy('display_chepareta')

    user_must_be_logged = True
    no_permission_redirect_to = 'display_chepareta'

    def form_valid(self, form):
        user = User.objects.filter(pk=self.request.user.pk).get()

        obj = form.save(commit=False)
        obj.created_by = user
        obj.save()

        return super().form_valid(form)


class ChepareDetailsView(DetailView):
    model = Chepare
    template_name = 'chepare-details.html'


class EditChepareView(RedirectLoggedUsersUrlTypers, UpdateView):
    model = Chepare
    fields = [field.name for field in model._meta.get_fields()[1:-3]]

    template_name = 'edit-chepare.html'
    success_url = reverse_lazy('display_chepareta')

    user_must_be_logged = True
    no_permission_redirect_to = 'display_chepareta'


class DeleteChepareView(RedirectLoggedUsersUrlTypers, DeleteView):
    model = Chepare
    template_name = 'delete-chepare.html'
    success_url = reverse_lazy('display_chepareta')

    user_must_be_logged = True
    no_permission_redirect_to = 'display_chepareta'
