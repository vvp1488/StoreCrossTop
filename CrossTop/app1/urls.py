from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    BaseView,
    DetailProductView,
    CartView,
    AddToCartView,
    DeleteFromCartView,
    CheckOutView,
    CategoryDetailView,
    LoginView,
    RegistrationView,
    ProfileView
)


urlpatterns = [
    path('',BaseView.as_view(), name = 'base'),
    path('products/<str:slug>', DetailProductView.as_view(), name ='product_detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<str:slug>', AddToCartView.as_view(), name='add_to_cart'),
    path('delete-from-cart/<str:slug>', DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('check-out/', CheckOutView.as_view(), name = 'check_out'),
    path('category/<str:slug>', CategoryDetailView.as_view(), name='category_detail'),
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/',ProfileView.as_view(), name='profile')
    ]
