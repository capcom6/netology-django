from django.urls import path

from .views import (
    MeasureCreateAPIView,
    SensorListCreateAPIView,
    SensorRetrieveUpdateAPIView,
)

urlpatterns = [
    path("sensors/", SensorListCreateAPIView.as_view()),
    path("sensors/<pk>/", SensorRetrieveUpdateAPIView.as_view()),
    path("measurements/", MeasureCreateAPIView.as_view()),
]
