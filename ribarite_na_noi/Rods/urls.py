from django.urls import path

from ribarite_na_noi.Rods.views import (DisplayRodsView,
                                        CreateRodView,
                                        RodDetailsView,
                                        EditRodView,
                                        DeleteRodView,
                                        )

urlpatterns = (
    path('', DisplayRodsView.as_view(), name='display_rods'),
    path('create_rod/', CreateRodView.as_view(), name='create_rod'),
    path('rod_details/<int:pk>/', RodDetailsView.as_view(), name='rod_details'),
    path('edit_rod/<int:pk>/', EditRodView.as_view(), name='edit_rod'),
    path('delete_rod/<int:pk>/', DeleteRodView.as_view(), name='delete_rod'),
)