from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render, redirect
from .models import Phone

ORDER = {
    "name": "name",
    "min_price": "price",
    "max_price": "-price",
}


def index(request):
    return redirect("catalog")


def show_catalog(request: HttpRequest):
    template = "catalog.html"

    sort = request.GET.get("sort", "name")
    order = ORDER.get(sort, "name")

    context = {
        "phones": Phone.objects.order_by(order).all(),
    }
    return render(request, template, context)


def show_product(request, slug):
    template = "product.html"

    phone = get_object_or_404(Phone, slug=slug)

    context = {
        "phone": phone,
    }
    return render(request, template, context)
