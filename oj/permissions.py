from rest_framework import permissions


# 用户权限
REGULAR_USER = 0
ADMIN = 1
SUPER_ADMIN = 2

class UserPermission(permissions.BasePermission):
    """用于用户 自己可以修改自己的信息，管理员可以修改用户信息，其他人不能修改"""
    def has_object_permission(self, request, view, obj):
        # 任何人都可以读取
        if request.method in permissions.SAFE_METHODS:
            return True
        try:
            if obj.id == request.user.id or request.user.user_type == ADMIN or request.user.user_type == SUPER_ADMIN:
                return True
        except Exception as error:
            return False
        return False

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        try:
            if request.user.user_type == ADMIN or request.user.user_type == SUPER_ADMIN:
                return True
        except Exception as error:
            return False
        return False

class IsSuperAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        try:
            if request.user.user_type == SUPER_ADMIN:
                return True
        except Exception as error:
            return False
        return False
