from django.urls import path

from . import views

urlpatterns = [
    path("login", views.login, name="login"),
    path("signup", views.signup, name="signup"),
    path("home", views.home, name="home"),
    path("product/<slug:slug>", views.motor_detail, name="motor-detail-page"),
    path("logout", views.logout, name="logout")
]
