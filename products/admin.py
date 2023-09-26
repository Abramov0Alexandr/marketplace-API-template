from django.contrib import admin
from products.models import Product


@admin.register(Product)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop_name', 'product_title', 'seller', 'price', )
    list_display_links = ('product_title', )
