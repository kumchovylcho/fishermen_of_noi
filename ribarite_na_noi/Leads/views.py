from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import (ListView,
                                  CreateView,
                                  DetailView,
                                  UpdateView,
                                  DeleteView,
                                  )

from ribarite_na_noi.Leads.forms import (SortLeadsForm,
                                         CreateLeadForm,
                                         FilterLeadsForm,
                                         )

from ribarite_na_noi.Leads.models import Lead
from ribarite_na_noi.common.validators import (RedirectNotAuthorizedUsers,
                                               RedirectNotAuthenticatedUsers,
                                               )


class DisplayLeadsView(ListView):
    template_name = 'display-leads.html'
    model = Lead

    @property
    def get_filter_options(self):
        return {"lead_type": Lead.LEAD_CHOICES[1:],
                "grams": Lead.GRAM_CHOICES[1:-1],
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
        context['sort_form'] = SortLeadsForm(self.request.GET)
        context['filters'] = FilterLeadsForm(self.request.GET)
        context['all_leads'] = Lead.objects.all()

        return context


class CreateLeadView(RedirectNotAuthenticatedUsers, CreateView):
    form_class = CreateLeadForm
    template_name = 'create-lead.html'
    success_url = reverse_lazy('display_leads')

    redirect_to = 'display_leads'

    def form_valid(self, form):
        user = User.objects.filter(pk=self.request.user.pk).get()

        obj = form.save(commit=False)
        obj.created_by = user
        obj.save()

        return super().form_valid(form)


class LeadDetailsView(DetailView):
    model = Lead
    template_name = 'lead-details.html'


class EditLeadView(RedirectNotAuthorizedUsers, UpdateView):
    model = Lead
    fields = [field.name for field in model._meta.get_fields()[1:-3]]

    template_name = 'edit-lead.html'
    success_url = reverse_lazy('display_leads')

    user_must_be_logged = True
    no_permission_redirect_to = 'display_leads'

    permission_required = 'Leads.change_lead'


class DeleteLeadView(RedirectNotAuthorizedUsers, DeleteView):
    model = Lead
    template_name = 'delete-lead.html'
    success_url = reverse_lazy('display_leads')

    user_must_be_logged = True
    no_permission_redirect_to = 'display_leads'

    permission_required = 'Leads.delete_lead'
