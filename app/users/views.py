from rest_framework import viewsets
from models import User
from serializers import UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated       # Delete maybe
from permissions import IsOwner
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import render

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]


#Achte darauf mit authentication und permission zua arbeiten hier ein bsp:
"""class ProtectedView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
"""
# IsAuthenticated brauchst du um zu kcuken ob der user über jwt token acces token hat und nur dann lässt du sachen zu!




