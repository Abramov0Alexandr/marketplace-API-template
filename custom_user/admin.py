from django.contrib import admin
from custom_user.models import CustomUser


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'is_seller', 'is_active', )
    list_display_links = ('email', )
    list_editable = ('is_seller', 'is_active', )
