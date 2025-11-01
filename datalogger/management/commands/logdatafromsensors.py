from django.core.management.base import BaseCommand
from django.conf import settings
from m5stack import QMP6988, SHT30, QMP6988Fake, SHT30Fake
from datalogger.models import Sensor, Measure

class Command(BaseCommand):
    help = ""

    def handle(self, *args, **options):

        if settings.SENSORS_ENABLED:
            qmp6988 = QMP6988()
            sht30 = SHT30()
        else:
            qmp6988 = QMP6988Fake()
            sht30 = SHT30Fake()

        enabled_sensors = Sensor.objects.all()

        data = list()
        for sensor in enabled_sensors:
            if sensor.code == 'M5STACK-ENV-3-UNIT-SHT30-TEMPERATURE':
                new_measure = Measure(
                    sensor=sensor,
                    value=sht30.read_temperature()
                )
                data.append(new_measure)

            if sensor.code == 'M5STACK-ENV-3-UNIT-SHT30-HUMIDITY':
                new_measure = Measure(
                    sensor=sensor,
                    value=sht30.read_humidity()
                )
                data.append(new_measure)

            if sensor.code == 'M5STACK-ENV-3-UNIT-QMP6988-PRESSURE':
                new_measure = Measure(
                    sensor=sensor,
                    value=qmp6988.read_pressure()
                )
                data.append(new_measure)

        Measure.objects.bulk_create(data)