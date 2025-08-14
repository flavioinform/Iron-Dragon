from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Profile
from .serializers import ProfileSerializer, RegisterSerializer
from rest_framework import status
from django.contrib.auth.models import Group

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Usuario creado correctamente"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserGroupsView(APIView):
    """
    Vista para obtener los grupos del usuario autenticado
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_groups = request.user.groups.all()
        groups_data = [{"id": group.id, "name": group.name} for group in user_groups]
        return Response(groups_data)