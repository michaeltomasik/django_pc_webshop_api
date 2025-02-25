from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated       # Delete maybe
from permissions import IsOwner


#Achte darauf mit authentication und permission zua arbeiten hier ein bsp:
"""class ProtectedView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
"""
# IsAuthenticated brauchst du um zu kcuken ob der user über jwt token acces token hat und nur dann lässt du sachen zu!




