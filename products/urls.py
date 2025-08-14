from django.urls import path
from .views import CategoryList, Categorydetail, ProductList, Productdetail, api_root

urlpatterns = [
    path('', api_root, name='api-root'),  # <- índice de la API
    path('categories/', CategoryList.as_view(), name='category-list'),
    path('categories/<int:pk>/', Categorydetail.as_view(), name='category-detail'),
    path('products/', ProductList.as_view(), name='product-list'),
    path('products/<int:pk>/', Productdetail.as_view(), name='product-detail'),
]
