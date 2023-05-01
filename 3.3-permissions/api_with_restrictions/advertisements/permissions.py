from rest_framework import permissions

from .models import AdvertisementStatusChoices


class IsAdvertisementCreator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user


class IsDraftCreatorOrAllow(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.status != AdvertisementStatusChoices.DRAFT:
            return True

        return obj.creator == request.user
