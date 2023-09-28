from django.urls import path

# import views
from .views import *


urlpatterns = [
    path("menu_item/", MenuItemList.as_view(), name="menu-item"),
    path("user_register/", Register.as_view(), name="user-register"),
    path("login/", Login.as_view(), name="user-login"),
    path(
        "initiate_oauth/<str:provider>/",
        OAuthLoginInitiatorView.as_view(),
        name="initiate-oauth",
    ),
    path(
        "authorize_oauth/<str:provider>/",
        OAuthLoginAuthorizeView.as_view(),
        name="authorize-oauth",
    ),
    path("logout/", Logout.as_view(), name="user-logout"),
    path("cart/", CartView.as_view(), name="cart"),
    path("cart_add/", CartMultiView.as_view(), name="cart-add"),
    path("cart_operation/<int:pk>", CartOperation.as_view(), name="cart-operation"),
    path("checkout/", SimpleCheckout.as_view(), name="checkout"),
    path("saveOrder/", SaveOrder.as_view(), name="save-order"),
]
