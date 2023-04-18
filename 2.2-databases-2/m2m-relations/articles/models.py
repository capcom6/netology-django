from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=256, verbose_name="Название")
    text = models.TextField(verbose_name="Текст")
    published_at = models.DateTimeField(verbose_name="Дата публикации")
    image = models.ImageField(
        null=True,
        blank=True,
        verbose_name="Изображение",
    )

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ["-published_at"]

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=64, verbose_name="Тег", unique=True)

    def save(self, *args, **kwargs) -> None:
        self.name = self.name.lower()

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ["name"]


class Scope(models.Model):
    article = models.ForeignKey(
        "Article",
        verbose_name="Статья",
        on_delete=models.CASCADE,
        related_name="scopes",
    )
    tag = models.ForeignKey("Tag", verbose_name="Тег", on_delete=models.CASCADE)
    is_main = models.BooleanField(verbose_name="Основной")

    class Meta:
        verbose_name = "Раздел"
        verbose_name_plural = "Разделы"
        ordering = ["-is_main", "tag__name"]
