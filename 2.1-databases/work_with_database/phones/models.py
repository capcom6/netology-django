from django.db import models
import django.utils.text as text


class Phone(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=11, decimal_places=2)
    image = models.URLField()
    release_date = models.DateField()
    lte_exists = models.BooleanField()
    slug = models.SlugField(max_length=64, unique=True)

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = text.slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name
