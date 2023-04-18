from rest_framework import serializers

from .models import Measure, Sensor


# TODO: опишите необходимые сериализаторы
class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ["id", "name", "description"]


class MeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measure
        fields = ["sensor", "temperature", "created_at"]


class SensorDetailsSerializer(serializers.ModelSerializer):
    measurements = MeasureSerializer(read_only=True, many=True)

    class Meta:
        model = Sensor
        fields = ["id", "name", "description", "measurements"]
