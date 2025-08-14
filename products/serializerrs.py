from rest_framework import serializers
from django_filters import rest_framework as filters
from .models import Product, Category


class ProductFilter(filters.FilterSet):
    category=filters.NumberFilter(field_name='category',lookup_expr='exact')
    #metodo para filtrar sin distincion 
    name=filters.CharFilter(method='filter_by_search', lookup_expr='icontains')
    
    def filter_by_search(self,queryset,value):
        return queryset.filter(name__icontains=value) |queryset.filter(description__icontains=value)
    
    class Meta:
        model = Product
        fields = {'category': ['exact'],
                 'name': ['icontains'] 
                  
                  
                  
                  }


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','name', 'description', 'slug', 'is_active', 'created_at', 'updated_at', 'image')


class ProductSerializer(serializers.ModelSerializer):
    # Para mostrar la categoría como objeto en lugar de solo el ID
    category_name=serializers.ReadOnlyField(source='category.name')
    
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    class Meta:
        model = Product
        fields = ('id', 'name','image', 'description', 'category_name','price', 'image', 'category', 'stock', 'is_active', 'created_at', 'updated_at')
        filterset_class=ProductFilter