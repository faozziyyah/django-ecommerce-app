from django.contrib import admin
from .models import Product, Category, Customer, Order, OrderItem, ShippingAddress, LikeProduct

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(LikeProduct)
