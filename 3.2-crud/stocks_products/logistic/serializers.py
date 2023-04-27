import typing
from django.db import transaction
from rest_framework import serializers

from .models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    # настройте сериализатор для продукта
    class Meta:
        model = Product
        fields = ["id", "title", "description"]


class ProductPositionSerializer(serializers.ModelSerializer):
    # настройте сериализатор для позиции продукта на складе
    class Meta:
        model = StockProduct
        fields = ["product", "price", "quantity"]


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    # настройте сериализатор для склада

    @transaction.atomic
    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop("positions")

        # создаем склад по его параметрам
        stock = super().create(validated_data)

        # здесь вам надо заполнить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions
        self._write_positions(stock, positions)

        return stock

    @transaction.atomic
    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop("positions")

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)

        # здесь вам надо обновить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions
        self._write_positions(stock, positions)

        return stock

    def _write_positions(
        self, stock: Stock, positions: typing.List[typing.OrderedDict[str, typing.Any]]
    ):
        StockProduct.objects.filter(stock=stock).delete()
        [StockProduct.objects.create(**p, stock=stock) for p in positions]

    class Meta:
        model = Stock
        fields = ["id", "address", "positions"]
