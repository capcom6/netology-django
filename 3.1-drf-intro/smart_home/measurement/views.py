from rest_framework import generics

from .models import Measure, Sensor
from .serializers import MeasureSerializer, SensorDetailsSerializer, SensorSerializer


# TODO: опишите необходимые обработчики, рекомендуется использовать generics APIView классы:
# TODO: ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView
class SensorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class SensorRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailsSerializer


class MeasureCreateAPIView(generics.CreateAPIView):
    queryset = Measure.objects.all()
    serializer_class = MeasureSerializer
