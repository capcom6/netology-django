from django.contrib.auth.models import AnonymousUser, User
from django.db.models import Q
from django_filters import rest_framework as filters
from rest_framework import permissions, response, status, viewsets
from rest_framework.decorators import action

from .exceptions import OpenAdvertisementsLimitException, SelfFavoriteException
from .filters import AdvertisementFilter
from .models import Advertisement, AdvertisementStatusChoices, Favorite
from .permissions import IsAdvertisementCreator, IsDraftCreatorOrAllow
from .serializers import AdvertisementSerializer


class AdvertisementViewSet(viewsets.ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects
    serializer_class = AdvertisementSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def get_queryset(self):
        where = ~Q(status="DRAFT")  # не показваем черновики
        if self.request.user.is_authenticated:
            where |= Q(creator=self.request.user)  # за исключением его создателя

        return self.queryset.filter(where)

    def create(self, request, *args, **kwargs):
        self._check_limit(request.user)
        return super().create(request, *args, **kwargs)

    def update(self, request, pk=None, *args, **kwargs):
        # при редактировании мы можем открывать ранее закрытые объявления
        # потому нужна проверка лимита и тут
        if request.data.get(status) == AdvertisementStatusChoices.OPEN:
            self._check_limit(request.user, pk)
        return super().update(request, pk, *args, **kwargs)

    @action(methods=["GET"], detail=False)
    def favorites(self, request):
        user = request.user
        serializer = self.get_serializer(
            [f.advertisement for f in user.favorites.all()], many=True
        )

        return response.Response(serializer.data)

    @action(methods=["POST", "DELETE"], detail=True, url_path="favorites")
    def edit_favorites(self, request, pk):
        favorite = Favorite.objects.filter(
            user=request.user, advertisement=self.get_object()
        )
        if request.method == "POST":
            if favorite.exists():
                return response.Response(status=status.HTTP_204_NO_CONTENT)

            if request.user == self.get_object().creator:
                raise SelfFavoriteException()

            Favorite.objects.create(user=request.user, advertisement=self.get_object())

            return response.Response(status=status.HTTP_201_CREATED)
        if request.method == "DELETE":
            if favorite.exists():
                favorite.delete()

            return response.Response(status=status.HTTP_204_NO_CONTENT)

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
        if self.action in ["favorites", "edit_favorites"]:
            return [permissions.IsAuthenticated()]

        if self.action in ["create"]:
            return [permissions.IsAuthenticated()]
        if self.action in ["update", "partial_update", "destroy"]:
            return [permissions.OR(IsAdvertisementCreator(), permissions.IsAdminUser())]
        return [IsDraftCreatorOrAllow()]
