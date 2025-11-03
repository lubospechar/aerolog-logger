from django.db import models


class Unit(models.Model):
    name = models.CharField(
        max_length=100,
    )
    symbol = models.CharField(
        max_length=10,
    )

    def __str__(self) -> str:
        if self.symbol:
            return f"{self.name} ({self.symbol})"
        return self.name


class Sensor(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(
        max_length=100,
    )
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    enabled = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.name} [{self.code}]"


class Measure(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    has_sent = models.BooleanField(default=False)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self) -> str:
        return f"{self.sensor.code} @ {self.timestamp:%Y-%m-%d %H:%M:%S} = {self.value}"