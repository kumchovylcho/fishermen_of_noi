from django.urls import path

from ribarite_na_noi.common.views import (HomeView,
                                          WelcomePageView,
                                          )

urlpatterns = (
    path('', HomeView.as_view(), name='home'),
    path('welcome/', WelcomePageView.as_view(), name='welcome-page'),
)