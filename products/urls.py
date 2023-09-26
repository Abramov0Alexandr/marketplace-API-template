from django.urls import path
from .apps import ProductsConfig
from .views import ProductCreateView, ProductDetailView, ProductListView, ProductDeleteView

app_name = ProductsConfig.name


urlpatterns = [
    path('create/', ProductCreateView.as_view(), name='create-product'),
    path('list/', ProductListView.as_view(), name='products-list'),
    path('detail/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='product-delete'),
    ]
