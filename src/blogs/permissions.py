from django.utils import timezone

from rest_framework.permissions import BasePermission


class PostPermission(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return request.user.is_superuser or request.user == obj.blog.user or obj.published_at <= timezone.now()
        else:
            return request.user.is_superuser or request.user == obj.blog.user
