# python
from django.contrib import admin
from .models import Unit, Sensor, Measure


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ("name", "symbol")
    search_fields = ("name", "symbol")
    ordering = ("name",)


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "unit", "enabled")
    search_fields = ("code", "name")
    list_select_related = ("unit",)
    ordering = ("code",)


@admin.register(Measure)
class MeasureAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "sensor", "value", "has_sent")
    list_filter = ("has_sent", "sensor")
    search_fields = ("sensor__code", "sensor__name")
    list_select_related = ("sensor", "sensor__unit")
    ordering = ("-timestamp",)