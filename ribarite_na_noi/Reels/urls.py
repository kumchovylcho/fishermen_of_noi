from django.urls import path

from ribarite_na_noi.Reels.views import (CreateReelView,
                                         DisplayReelsView,
                                         ReelDetailsView,
                                         EditReelView,
                                         DeleteReelView,
                                         )

urlpatterns = (
    path('', DisplayReelsView.as_view(), name='display_reels'),
    path('create_reel/', CreateReelView.as_view(), name='create_reel'),
    path('reel_details/<int:pk>/', ReelDetailsView.as_view(), name='reel_details'),
    path('edit_reel/<int:pk>/', EditReelView.as_view(), name='edit_reel'),
    path('delete_reel/<int:pk>/', DeleteReelView.as_view(), name='delete_reel'),
)