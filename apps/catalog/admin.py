from django.contrib import admin

from .models import Brand, Category, Coupon, Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "brand", "category", "price", "compare_at_price", "stock", "is_active"]
    list_filter = ["category", "brand", "family", "is_active"]
    search_fields = ["name", "brand__name"]
    prepopulated_fields = {"slug": ["name"]}
    inlines = [ProductImageInline]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ["name", "country", "is_featured"]
    prepopulated_fields = {"slug": ["name"]}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "order"]
    prepopulated_fields = {"slug": ["name"]}


admin.site.register(Coupon)
