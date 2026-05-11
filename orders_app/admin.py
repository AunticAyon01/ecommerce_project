from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'product', 'quantity', 'total_price', 'status', 'order_date']
    list_filter = ['status']
    search_fields = ['user__username', 'product__product_name']
