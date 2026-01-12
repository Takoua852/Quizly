from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Allows access only to the owner of the object.
    Expects the object to have a `user` attribute.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
