from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrStoreManagerOrOwner(BasePermission):
    """
    Custom permission class to allow access based on user roles.
    """

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
            if request.user.role in ["store_owner", "store_manager"]:
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
            "store_manager",
        ]:
            # Assuming `obj` is a product and has a `store` relation
            return obj.store.owner == request.user or obj.store.manager == request.user

        # Allow read-only access for other users
        if request.method in SAFE_METHODS:
            return True

        # Deny access by default
        return False


# class IsAdminOrStoreManagerOrOwner(BasePermission):
#     def has_permission(self, request, view):
#         # Allow read access to all users (including unauthenticated ones)
#         if request.method in ["GET", "HEAD", "OPTIONS"]:
#             return True

#         # If the user is authenticated, check their role
#         if request.user.is_authenticated:
#             # Allow admin to do everything
#             if request.user.role == "admin":
#                 return True

#             # Allow store owner/manager to access their store's products
#             if request.user.role in ["store_owner", "store_manager"]:
#                 return True

#         # Deny permission for other users (including unauthenticated for non-read actions)
#         return False

#     def has_object_permission(self, request, view, obj):
#         # Admin can do anything
#         if request.user.is_authenticated and request.user.role == "admin":
#             return True

#         # Store owner/manager can only access their store's products
#         if request.user.is_authenticated and request.user.role in [
#             "store_owner",
#             "store_manager",
#         ]:
#             return obj.store.owner == request.user or obj.store.manager == request.user

#         # Allow read access to unauthenticated users or customers for viewing product details
#         # (customers are typically those who are authenticated but not admin or store roles)
#         if request.method in ["GET", "HEAD", "OPTIONS"]:
#             return True

#         # Deny access for others
#         return False
