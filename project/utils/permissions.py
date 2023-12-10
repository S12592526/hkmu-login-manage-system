
from rest_framework.permissions import BasePermission
import json
from django.middleware.csrf import get_token, rotate_token


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        """针对每一次请求的权限检查"""
        if request.user:
            return True

    def has_object_permission(self, request, view, obj):
        return True
