# datalogger/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from datalogger.views import MeasureViewSet


router = DefaultRouter()
router.register(r"measures", MeasureViewSet, basename="measure")

urlpatterns = [
    path("", include(router.urls)),
]
