from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetView
from django.urls import path

from .views import PasswordChangeView, UserCreateView, UserListView, UserUpdateView

urlpatterns = [
    path("users/", UserListView.as_view(), name="user_list"),
    path("register/", UserCreateView.as_view(), name="user_register"),
    path("profile/update/", UserUpdateView.as_view(), name="profile_update"),
    path("password/change/", PasswordChangeView.as_view(), name="password_change"),
    path("password/reset/", PasswordResetView.as_view(), name="password_reset"),
    path(
        "password/reset/confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
]
