from rest_framework import permissions


class MyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # referer
        if request.META.get('HTTP_REFERER'):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        # 验证某个对象符不符合某些情况
        # 例如：商家 名称中 有 之 字 才能去访问
        if '之' in obj.name:
            return True
        else:
            return False
