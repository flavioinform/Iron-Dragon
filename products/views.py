from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import BasePermission
from .models import Product, Category
from .serializerrs import CategorySerializer, ProductSerializer

# Permiso personalizado
class IsAdminGroup(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='administrador').exists()

# Endpoint raíz
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        "categories": request.build_absolute_uri('categories/'),
        "products": request.build_absolute_uri('products/')
    })

# Categorías
class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class Categorydetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# Productos
class ProductList(generics.ListCreateAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        # filtrar por nombre
        search = self.request.query_params.get('search', None)
        if search is not None:
            queryset = queryset.filter(name__icontains=search) | queryset.filter(description__icontains=search)
        return queryset

    # Solo administradores pueden crear productos
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminGroup()]
        return super().get_permissions()

class Productdetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # Solo administradores pueden editar/eliminar productos
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdminGroup()]
        return super().get_permissions()