# coding=utf-8

import datetime
from django.db import models


class Book(models.Model):
    name = models.CharField(u'Название', max_length=64)
    author = models.CharField(u'Автор', max_length=64)
    pub_date = models.DateField(u'Дата публикации')

    def __str__(self):
        return self.name + " " + self.author

    @classmethod
    def select(cls, date: datetime.date|None = None):
        query = cls.objects

        if date:
            query = query.filter(pub_date=date)

        return query.all()

    @classmethod
    def get_next_date(cls, date: datetime.date) -> datetime.date | None:
        return cls.objects.values_list('pub_date', flat=True).filter(pub_date__gt=date).order_by('pub_date').first()
    
    @classmethod
    def get_prev_date(cls, date: datetime.date) -> datetime.date | None:
        return cls.objects.values_list('pub_date', flat=True).filter(pub_date__lt=date).order_by('-pub_date').first()