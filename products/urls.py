from django.urls import path
from .apps import ProductsConfig
from .views import ProductCreateView, ProductDetailView, ProductListView, ProductDeleteView, ChangeProductSaleStatus

app_name = ProductsConfig.name


urlpatterns = [
    path('create/', ProductCreateView.as_view(), name='create-product'),
    path('list/', ProductListView.as_view(), name='products-list'),
    path('change_status/<int:pk>/', ChangeProductSaleStatus.as_view(), name='change-status'),
    path('detail/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='product-delete'),
    ]
