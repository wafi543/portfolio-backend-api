from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Allow access only to the owner of the object."""

    def has_object_permission(self, request, view, obj):
        return getattr(obj, 'author_id', None) == request.user.id
