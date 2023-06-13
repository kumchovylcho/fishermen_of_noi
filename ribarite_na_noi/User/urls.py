from django.urls import path

from ribarite_na_noi.User.views import (UserLoginView,
                                        UserRegisterView,
                                        LogOut,
                                        ProfileView,
                                        ChangePassword,
                                        SuccessPasswordChange,
                                        ChangeUsername,
                                        SuccessUsernameChange,
                                        DeleteUser,
                                        )

urlpatterns = (
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('logout/', LogOut.as_view(), name='logout'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/change_password/', ChangePassword.as_view(), name='change_password'),
    path('success_change_password/', SuccessPasswordChange.as_view(), name='successful_password_change'),
    path('success_change_username/', SuccessUsernameChange.as_view(), name='successful_username_change'),
    path('profile/<int:pk>/change_username/', ChangeUsername.as_view(), name='change_username'),
    path('profile/<int:pk>/delete/', DeleteUser.as_view(), name='delete_user'),
)