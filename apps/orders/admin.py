from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["__str__", "full_name", "status", "total", "created_at"]
    list_filter = ["status", "shipping_method", "payment_method"]
    search_fields = ["full_name", "email"]
    inlines = [OrderItemInline]
