from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """If the user is owner of the data he can request it."""
    def has_object_permission(self, request, view, obj):
        return obj.created.by == request.user