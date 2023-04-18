from django.db import models
from django.utils.translation import gettext as _


# TODO: опишите модели датчика (Sensor) и измерения (Measurement)
class Sensor(models.Model):
    name = models.CharField(_("Name"), max_length=64)
    description = models.TextField(_("Description"), blank=True)

    class Meta:
        verbose_name = _("Sensor")
        verbose_name_plural = _("Sensors")

    def __str__(self):
        return self.name


class Measure(models.Model):
    sensor = models.ForeignKey(
        "Sensor",
        verbose_name=_("Sensor"),
        on_delete=models.RESTRICT,
        related_name="measurements",
    )
    temperature = models.DecimalField(_("Temperature"), max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(
        _("Date and time"), auto_now=False, auto_now_add=True
    )

    class Meta:
        verbose_name = _("Measure")
        verbose_name_plural = _("Measures")

    def __str__(self):
        return f"{self.temperature} at {self.created_at}"
