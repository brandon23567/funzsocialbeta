from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register_user/", views.registerUser, name="registerUser"),
    path("login_user/", views.login_user, name="login_user"),
    path("get_current_user/", views.get_current_user, name="get_current_user"),
    path("refresh_token/", views.refresh_token, name="refresh_token"),
]
