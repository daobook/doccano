from rest_framework.permissions import BasePermission


class IsOwnComment(BasePermission):
    @classmethod
    def has_object_permission(cls, request, view, obj):
        return True if request.user.is_superuser else obj.user.id == request.user.id
