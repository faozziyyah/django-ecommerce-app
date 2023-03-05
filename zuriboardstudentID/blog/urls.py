from django.urls import path
from . import views

urlpatterns = [
    path('', views.signin, name='login'),
    path('index', views.index, name='index'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('settings', views.settings, name='settings'),
    path('signup', views.signup, name='register'),
    path('logout', views.logout, name='logout'),
    path('add_to_cart/', views.addToCart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('process_order/', views.processOrder, name='process_order'),
    path('show_product/<product_id>', views.show_product, name='show-product'),
    path('delete_cart/<order_id>', views.delete_cart, name='delete-cart'),
    path('like-product', views.like_product, name='like-product'),
    path('search_product', views.search_product, name='search-product'),
    path('show_category/<category_id>', views.show_category, name='show-category'),
]