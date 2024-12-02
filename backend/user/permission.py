from rest_framework.permissions import BasePermission

class IsBerlinUnited(BasePermission):
    """
    Permission class to check if a user's organization matches a specific value.
    """
    def has_permission(self, request, view):
        # Ensure the user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Check the user's organization (replace with your condition)
        return request.user.organization and request.user.organization.name == "berlin_united"