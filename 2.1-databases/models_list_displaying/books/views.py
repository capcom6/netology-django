import datetime
from typing import Any
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from books.models import Book


def index_view(request: HttpRequest) -> HttpResponse:
    return HttpResponseRedirect(reverse('books'))

def books_view(request, date: datetime.date|None = None):
    template = 'books/books_list.html'
    context: dict[str, Any] = {
        "books": Book.select(date),
    }
    if date:
        context["date_next"] = Book.get_next_date(date)
        context["date_prev"] = Book.get_prev_date(date)
    return render(request, template, context)
