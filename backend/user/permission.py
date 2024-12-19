from rest_framework.permissions import BasePermission,SAFE_METHODS

class IsBerlinUnited(BasePermission):
    """
    Permission class to check if a user's organization matches a specific value.
    """
    def has_permission(self, request, view):
        # Ensure the user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False
        
        # check if user is member of berlin_united
        return request.user.organization and request.user.organization.name == "berlin_united"


class IsBerlinUnitedOrReadOnly(BasePermission):
    """
    Allows authenticated users to retrieve data and BU Users to modify data
    """
    def has_permission(self, request, view):
        # Ensure the user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Allows request if it's a GET HEAD or OPTIONS Request
        if request.method in SAFE_METHODS:
            return True

        # check if user is member of berlin_united
        return request.user.organization and request.user.organization.name == "berlin_united"
