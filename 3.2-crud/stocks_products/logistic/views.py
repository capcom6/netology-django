from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # при необходимости добавьте параметры фильтрации
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "description"]


class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    # при необходимости добавьте параметры фильтрации
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["products"]
    search_fields = ["products__title"]
