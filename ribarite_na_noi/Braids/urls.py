from django.urls import path

from ribarite_na_noi.Braids.views import (DisplayBraidsView,
                                          CreateBraidView,
                                          BraidDetailsView,
                                          EditBraidView,
                                          DeleteBraidView,
                                          )

urlpatterns = (
    path('', DisplayBraidsView.as_view(), name='display_braids'),
    path('create_braid/', CreateBraidView.as_view(), name='create_braid'),
    path('braid_details/<int:pk>', BraidDetailsView.as_view(), name='braid_details'),
    path('edit_braid/<int:pk>', EditBraidView.as_view(), name='edit_braid'),
    path('delete_braid/<int:pk>', DeleteBraidView.as_view(), name='delete_braid'),
)