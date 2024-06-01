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
    path("cart/change-quantity", views.change_cart_item_quantity, name="change-cart-item-quantity"),
    path("order/order-list", views.order_list, name="order-list"),
    path("order/detail/<int:order_id>", views.order_detail, name="order-detail"),
    path("order/order-bill-download/<int:order_id>", views.order_bill_download, name="order-bill-download"),
    path("search", views.search_engine, name='search'),
    path("search/brand/<int:brand_id>", views.search_brand, name="search-brand"),
    path("search/type/<int:type_id>", views.search_type, name="search-type"),
    path("user/update-info", views.update_user_info, name='update-user-info')
]
