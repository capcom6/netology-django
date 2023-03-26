import csv

from django.core.management.base import BaseCommand
from django.db import transaction
from phones.models import Phone


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open("phones.csv", "r") as file:
            phones = list(csv.DictReader(file, delimiter=";"))

        with transaction.atomic():
            for phone in phones:
                Phone.objects.update_or_create(**phone)
