from django.contrib import admin
from custom_user.models import CustomUser


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_seller', )
    list_display_links = ('email', )
    list_filter = ('is_seller', )
