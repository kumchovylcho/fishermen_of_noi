from django.urls import path

from ribarite_na_noi.Chepareta.views import (DisplayCheparetaView,
                                             CreateChepareView,
                                             ChepareDetailsView,
                                             EditChepareView,
                                             DeleteChepareView,
                                             )

urlpatterns = (
    path('', DisplayCheparetaView.as_view(), name='display_chepareta'),
    path('create_chepare/', CreateChepareView.as_view(), name='create_chepare'),
    path('chepare_details/<int:pk>', ChepareDetailsView.as_view(), name='chepare_details'),
    path('edit_chepare/<int:pk>', EditChepareView.as_view(), name='edit_chepare'),
    path('delete_chepare/<int:pk>', DeleteChepareView.as_view(), name='delete_chepare'),
)