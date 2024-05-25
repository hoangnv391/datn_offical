from django.urls import path

from . import views

urlpatterns = [
    path("login", views.login, name="login"),
    path("signup", views.signup, name="signup"),
    path("home", views.home, name="home"),
    path("product/<slug:slug>", views.motor_detail, name="motor-detail-page"),
    path("logout", views.logout, name="logout"),
    path("product/product/add-to-cart", views.add_to_cart, name='add-to-cart'),
    path("product/cart/add-to-cart", views.add_to_cart, name='add-to-cart'),
    path("cart", views.cart, name="cart"),
]
