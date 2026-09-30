from django.urls import path
from . import views
from . import api_views

urlpatterns = [
    path("", views.index, name="home"),
    path("shop/", views.shop, name="shop"),
    path("contact/", views.contact, name="contact"),
    path("product/<int:id>/", views.product, name="product"),
    path("cart/",views.cart,name="cart"),
    path("add-to-cart/<int:game_id>/", views.add_to_cart, name="add_to_cart"),
    path("register/", views.register, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path(
    "cart/increase/<int:item_id>/",views.increase_quantity,name="increase_quantity"),

    path(
    "cart/decrease/<int:item_id>/",views.decrease_quantity,name="decrease_quantity"),

    path("cart/remove/<int:item_id>/",views.remove_item,name="remove_item"),
    path("checkout/",views.checkout,name="checkout"),
    path('payment/', views.payment, name='payment'),
    path('api/cart/', api_views.api_cart_detail, name='api_cart_detail'),
    path('api/cart/add/<int:game_id>/', api_views.api_add_to_cart, name='api_add_to_cart'),
    path('api/cart/increase/<int:item_id>/', api_views.api_increase_quantity, name='api_increase_quantity'),
    path('api/cart/decrease/<int:item_id>/', api_views.api_decrease_quantity, name='api_decrease_quantity'),
    path('api/cart/remove/<int:item_id>/', api_views.api_remove_item, name='api_remove_item'),
    path('api/search/', api_views.api_search_games, name='api_search_games'),

]