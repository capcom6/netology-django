from django.contrib.auth.models import User
from django_filters import rest_framework as filters
from rest_framework import permissions, viewsets

from .exceptions import OpenAdvertisementsLimitException
from .filters import AdvertisementFilter
from .models import Advertisement, AdvertisementStatusChoices
from .serializers import AdvertisementSerializer


class IsAdvertisementCreator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.creator == request.user


class AdvertisementViewSet(viewsets.ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def create(self, request, *args, **kwargs):
        self._check_limit(request.user)
        return super().create(request, *args, **kwargs)

    def update(self, request, pk=None, *args, **kwargs):
        # при редактировании мы можем открывать ранее закрытые объявления
        # потому нужна проверка лимита и тут
        self._check_limit(request.user, pk)
        return super().update(request, pk, *args, **kwargs)

    def _check_limit(self, user: User, exclude=None) -> None:
        count = (
            Advertisement.objects.filter(
                creator=user, status=AdvertisementStatusChoices.OPEN
            )
            .exclude(
                pk=exclude
            )  # необходимо исключить текущее редактируемое объявление
            .count()
        )
        if count >= 10:
            raise OpenAdvertisementsLimitException

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create"]:
            return [permissions.IsAuthenticated()]
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAdvertisementCreator()]
        return []
