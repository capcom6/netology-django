from django.urls import path, register_converter

from .converters import DateConverter
from .views import books_view, index_view

register_converter(DateConverter, 'date')

urlpatterns = [
    path('', index_view, name='index'),
    path('books/', books_view, name='books'),
    path('books/<date:date>', books_view, name='books_by_date'),
]