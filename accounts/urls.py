# En tu archivo urls.py de la app de usuarios
from django.urls import path
from .views import ProfileView, RegisterView, UserGroupsView

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('groups/', UserGroupsView.as_view(), name='user-groups'),
]