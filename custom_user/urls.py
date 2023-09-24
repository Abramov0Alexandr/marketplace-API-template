from django.urls import path
from .apps import CustomUserConfig
from .views import CustomUserListView, CustomUserCreateView


app_name = CustomUserConfig.name


urlpatterns = [
    path('', CustomUserListView.as_view(), name='custom_user_list'),
    path('create/', CustomUserCreateView.as_view(), name='custom_user_create')
    ]
