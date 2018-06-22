from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsSubmitterOrReadOnly(BasePermission):
    message = "You are not the submitter of this book."

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.submitter == request.user
