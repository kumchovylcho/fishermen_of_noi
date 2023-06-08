from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import (CreateView,
                                  ListView,
                                  DetailView,
                                  UpdateView,
                                  DeleteView,
                                  )

from ribarite_na_noi.Rods.forms import (CreateRodForm,
                                        SortRodsForm,
                                        FilterRodsForm
                                        )
from ribarite_na_noi.Rods.models import Rod
from ribarite_na_noi.common.validators import (RedirectNotAuthorizedUsers,
                                               RedirectNotAuthenticatedUsers,
                                               )


class DisplayRodsView(SortRodsForm, ListView):
    template_name = 'display-rods.html'
    model = Rod

    @property
    def get_filter_options(self):
        return {"rod_type": Rod.ROD_TYPE_CHOICES[1:-1],
                "action": Rod.ROD_ACTION_CHOICES[1:-1],
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
        ordering = self.request.GET.get('sort_by', '-length')

        if "clear_filters" in self.request.GET:
            self.request.GET = self.request.GET.copy()
            self.request.GET.pop("filter_by")
            self.request.GET.pop("clear_filters")

        elif "clear_filters" not in self.request.GET:
            filter_atr = self.get_filter_atr(user_filter)
            if filter_atr:
                queryset = queryset.filter(**{filter_atr: user_filter})

        return queryset.order_by(ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort_form'] = SortRodsForm(self.request.GET)
        context['filters'] = FilterRodsForm(self.request.GET)
        context['all_rods'] = Rod.objects.all()

        return context


class CreateRodView(RedirectNotAuthenticatedUsers, CreateView):
    form_class = CreateRodForm
    template_name = 'create-rod.html'
    success_url = reverse_lazy('display_rods')

    redirect_to = 'display_rods'

    def form_valid(self, form):
        user = User.objects.filter(pk=self.request.user.pk).get()

        obj = form.save(commit=False)
        obj.created_by = user
        obj.save()

        return super().form_valid(form)


class RodDetailsView(DetailView):
    model = Rod
    template_name = 'rod-details.html'


class EditRodView(RedirectNotAuthorizedUsers, UpdateView):
    model = Rod
    fields = ("rod_type",
              "length",
              "guides",
              "rod_name",
              "action",
              "color",
              "price",
              "image"
              )

    template_name = 'edit-rod.html'
    success_url = reverse_lazy('display_rods')

    user_must_be_logged = True
    no_permission_redirect_to = 'display_rods'

    permission_required = "Rods.change_rod"


class DeleteRodView(RedirectNotAuthorizedUsers, DeleteView):
    model = Rod
    template_name = 'delete-rod.html'
    success_url = reverse_lazy('display_rods')

    user_must_be_logged = True
    no_permission_redirect_to = 'display_rods'

    permission_required = "Rods.delete_rod"
