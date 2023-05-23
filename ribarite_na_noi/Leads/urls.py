from django.urls import path

from ribarite_na_noi.Leads.views import (DisplayLeadsView,
                                         CreateLeadView,
                                         LeadDetailsView,
                                         EditLeadView,
                                         DeleteLeadView,
                                         )

urlpatterns = (
    path('', DisplayLeadsView.as_view(), name='display_leads'),
    path('create_lead/', CreateLeadView.as_view(), name='create_lead'),
    path('lead_details/<int:pk>', LeadDetailsView.as_view(), name='lead_details'),
    path('edit_lead/<int:pk>', EditLeadView.as_view(), name='edit_lead'),
    path('delete_lead/<int:pk>', DeleteLeadView.as_view(), name='delete_lead'),
)
