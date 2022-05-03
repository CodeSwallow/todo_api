from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == get_object_or_404(User, pk=request.user.id)


class IsListOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.list_id.owner == get_object_or_404(User, pk=request.user.id)
