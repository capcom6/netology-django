from django.contrib.auth.models import User
from rest_framework import exceptions, serializers, request

from .exceptions import OpenAdvertisementsLimitException
from .models import Advertisement, AdvertisementStatusChoices


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
        )


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = (
            "id",
            "title",
            "description",
            "creator",
            "status",
            "created_at",
        )

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        # С моей точки зрения помещать сюда проверку количества открытых объявлений некорректно
        # поскольку это по сути своей не валидация входящих данных, а бизнес-логика
        # Дополнительно к этому сериализатор может использовать не только в контексте создания/редактирования объявлений,
        # но и в других запросах, где проверка по кол-ву открытых объявлений лишняя
        # Плюс для корректной проверки кол-ва объявлений надо знать, происходит ли создание нового объявление или редактирование существующего.
        # При редактировании нам надо исключить из подсчета редактируемое объявление, но в рамках данного метода реализация будет не очевидной
        # Если опустить все эти моменты, то проверка будет "тупой" не позволяя отредактировать открытое объявление при наличии 10 открытых
        return data
