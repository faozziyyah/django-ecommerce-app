from django.urls import path
from . import views

urlpatterns = [
    path('', views.signin, name='login'),
    path('index', views.index, name='index'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('settings', views.settings, name='settings'),
    path('signup', views.signup, name='register'),
    path('logout', views.logout, name='logout'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
]