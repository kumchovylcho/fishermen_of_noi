from django.urls import path

from ribarite_na_noi.User.views import (UserLoginView,
                                        UserRegisterView,
                                        LogOut,
                                        )

urlpatterns = (
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('logout/', LogOut.as_view(), name='logout'),
)