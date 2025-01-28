from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrStoreManagerOrOwner(BasePermission):

    def has_permission(self, request, view):
        # Allow safe methods (GET, HEAD, OPTIONS) for everyone
        if request.method in SAFE_METHODS:
            return True

        # Ensure the user is authenticated
        if request.user.is_authenticated:
            # Admins can access everything
            if request.user.role == "admin":
                return True

            # Store owners and managers can access non-safe methods
            if request.user.role in ["store_owner", "admin"]:
                return True

        # Deny access for everyone else
        return False

    def has_object_permission(self, request, view, obj):
        # Admins have full access to all objects
        if request.user.is_authenticated and request.user.role == "admin":
            return True

        # Store owners/managers can only access objects linked to their store
        if request.user.is_authenticated and request.user.role in [
            "store_owner",
            "admin",
        ]:
            # Assuming `obj` is a product and has a `store` relation
            return obj.store.owner == request.user

        # Allow read-only access for other users
        if request.method in SAFE_METHODS:
            return True

        # Deny access by default
        return False


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role == "admin":
                return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user.role == "admin":
            return True
        return False
