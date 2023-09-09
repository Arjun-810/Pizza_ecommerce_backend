from django.urls import path

# import views
from .views import *


urlpatterns = [
    path('menu_item/', MenuItemList.as_view(), name="menu-item"),
    path('user_register/', Register.as_view(), name="user-register"),
    path('login/', Login.as_view(), name="user-register"),
]