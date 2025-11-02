# datalogger/serializers.py
from rest_framework import serializers
from .models import Measure

class MeasureSerializer(serializers.ModelSerializer):
    sensor = serializers.CharField(source="sensor.code", read_only=True)

    class Meta:
        model = Measure
        fields = ("id", "sensor", "value", "timestamp")
        read_only_fields = ("id", "sensor", "value", "timestamp")