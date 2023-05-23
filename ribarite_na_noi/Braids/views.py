from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (ListView,
                                  CreateView,
                                  DetailView,
                                  UpdateView,
                                  DeleteView,
                                  )

from ribarite_na_noi.Braids.forms import (SortBraidsForm,
                                          CreateBraidForm,
                                          FilterBraidsForm,
                                          )
from ribarite_na_noi.Braids.models import Braid
from ribarite_na_noi.common.validators import (RedirectNotLoggedUsers,
                                               RedirectLoggedUsersUrlTypers,
                                               )


class DisplayBraidsView(ListView):
    template_name = 'display-braids.html'
    model = Braid

    @property
    def get_filter_options(self):
        return {"thickness": Braid.THICKNESS_CHOICES[1:-1],
                "strength": Braid.STRENGTH_CHOICES[1:-1],
                "length": Braid.LENGTH_CHOICES[1:],
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
        ordering = self.request.GET.get('sort_by', '-price')

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
        context['sort_form'] = SortBraidsForm(self.request.GET)
        context['filters'] = FilterBraidsForm(self.request.GET)
        context['all_braids'] = Braid.objects.all()

        return context


class CreateBraidView(RedirectNotLoggedUsers, CreateView):
    form_class = CreateBraidForm
    template_name = 'create-braid.html'
    success_url = reverse_lazy('display_braids')

    user_must_be_logged = True
    no_permission_redirect_to = 'display_braids'

    def form_valid(self, form):
        user = User.objects.filter(pk=self.request.user.pk).get()

        obj = form.save(commit=False)
        obj.created_by = user
        obj.save()

        return super().form_valid(form)


class BraidDetailsView(DetailView):
    model = Braid
    template_name = 'braid-details.html'


class EditBraidView(RedirectLoggedUsersUrlTypers, UpdateView):
    model = Braid
    fields = [field.name for field in model._meta.get_fields()[1:-3]]

    template_name = 'edit-braid.html'
    success_url = reverse_lazy('display_braids')

    user_must_be_logged = True
    no_permission_redirect_to = 'display_braids'


class DeleteBraidView(RedirectLoggedUsersUrlTypers, DeleteView):
    model = Braid
    template_name = 'delete-braid.html'
    success_url = reverse_lazy('display_braids')

    user_must_be_logged = True
    no_permission_redirect_to = 'display_braids'
