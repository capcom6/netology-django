import csv

from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse


CONTENT = []
with open(settings.BUS_STATION_CSV, encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    CONTENT = [v for v in reader]


def index(request):
    return redirect(reverse("bus_stations"))


def bus_stations(request: HttpRequest):
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице

    page_number = request.GET.get("page", 1)
    pagi = Paginator(CONTENT, 10)
    page = pagi.get_page(page_number)

    context = {
        "bus_stations": page.object_list,
        "page": page,
    }
    return render(request, "stations/index.html", context)
