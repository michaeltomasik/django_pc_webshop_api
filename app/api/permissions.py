from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff


class IsAdminOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.created_by == request.user


from rest_framework.permissions import BasePermission









class IsSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user  # Jeder sieht nur sich selbst




from rest_framework.permissions import IsAuthenticated
from .permissions import IsSelf

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Jeder muss eingeloggt sein

    def get_queryset(self):
        """Nur der eingeloggte Nutzer sieht seine eigenen Daten."""
        return User.objects.filter(id=self.request.user.id)