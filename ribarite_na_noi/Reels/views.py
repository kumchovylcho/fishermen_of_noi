from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (ListView,
                                  CreateView,
                                  DetailView,
                                  UpdateView,
                                  DeleteView,
                                  )

from ribarite_na_noi.Reels.forms import (CreateReelForm,
                                         SortReelsForm,
                                         FilterReelsForm,
                                         )
from ribarite_na_noi.Reels.models import Reel
from ribarite_na_noi.common.validators import RedirectNotLoggedUsers


class DisplayReelsView(ListView):
    template_name = 'display-reels.html'
    model = Reel

    @property
    def get_filter_options(self):
        return {"size": Reel.SIZE_CHOICES[1:-1],
                "gear_ratio": Reel.GEAR_RATIO_CHOICES[1:-1],
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
        ordering = self.request.GET.get('sort_by', '-size')

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
        context['sort_form'] = SortReelsForm(self.request.GET)
        context['filters'] = FilterReelsForm(self.request.GET)
        context['all_reels'] = Reel.objects.all()

        return context


class CreateReelView(RedirectNotLoggedUsers, CreateView):
    form_class = CreateReelForm
    template_name = 'create-reel.html'
    success_url = reverse_lazy('display_reels')

    user_must_be_logged = True
    no_permission_redirect_to = 'display_reels'

    def form_valid(self, form):
        user = User.objects.filter(pk=self.request.user.pk).get()

        obj = form.save(commit=False)
        obj.created_by = user
        obj.save()

        return super().form_valid(form)


class ReelDetailsView(DetailView):
    model = Reel
    template_name = 'reel-details.html'


class EditReelView(RedirectNotLoggedUsers, UpdateView):
    model = Reel
    fields = [field.name for field in model._meta.get_fields()[1:-3]]

    template_name = 'edit-reel.html'
    success_url = reverse_lazy('display_reels')

    user_must_be_logged = True
    no_permission_redirect_to = 'display_reels'


class DeleteReelView(RedirectNotLoggedUsers, DeleteView):
    model = Reel
    template_name = 'delete-reel.html'
    success_url = reverse_lazy('display_reels')

    user_must_be_logged = True
    no_permission_redirect_to = 'display_reels'

