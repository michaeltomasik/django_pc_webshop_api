from rest_framework import viewsets
from models import User
from serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from permissions import IsOwner

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    ordering = ['created_at']




