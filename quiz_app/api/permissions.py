from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Custom permission to allow access only to the owner of an object.

    Responsibilities:
    - Used in DRF views to restrict object-level access
    - Ensures that only the user who owns the object can retrieve,
      update, or delete it

    Example usage in a view:
        permission_classes = [IsOwner, IsAuthenticated]
    """
    def has_object_permission(self, request, view, obj):
        """
        Check if the requesting user is the owner of the object.

        Args:
            request (Request): The HTTP request instance
            view (View): The DRF view instance
            obj (Model): The object to check ownership for, expected
                         to have a `user` attribute

        Returns:
            bool: True if the requesting user is the owner, else False
        """
        return obj.user == request.user
