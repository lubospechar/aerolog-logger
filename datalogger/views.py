from rest_framework.views import APIView
from rest_framework.response import Response
from datalogger.serializers import MeasureSerializer

# views.py
from rest_framework import viewsets
from .models import Measure

class MeasureViewSet(viewsets.ModelViewSet):
    serializer_class = MeasureSerializer
    def get_queryset(self):
        return (
            Measure.objects
            .filter(has_sent=False)
            .select_related("sensor")
            .order_by("timestamp")
        )