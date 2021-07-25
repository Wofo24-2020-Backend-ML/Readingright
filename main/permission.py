from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS
from .models import *


class IsUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user.id == request.user.id

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.admin

class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class IsAdminorReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = User.objects.filter(pk=request.user.id, admin = True)
        if user:
            return True
        return False

class IsAdminorIsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.user.id == request.user.id or request.user.is_admin:
            return True
        else:
            return False