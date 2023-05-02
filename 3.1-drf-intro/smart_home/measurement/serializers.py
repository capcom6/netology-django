import base64
from rest_framework import serializers, fields

from .models import Measure, Sensor


# TODO: опишите необходимые сериализаторы
class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ["id", "name", "description"]


class MeasureSerializer(serializers.ModelSerializer):
    photo = fields.ImageField(
        required=False, max_length=None, allow_empty_file=True, use_url=True
    )

    class Meta:
        model = Measure
        fields = ["sensor", "temperature", "created_at", "photo"]


class SensorDetailsSerializer(serializers.ModelSerializer):
    measurements = MeasureSerializer(read_only=True, many=True)

    class Meta:
        model = Sensor
        fields = ["id", "name", "description", "measurements"]
