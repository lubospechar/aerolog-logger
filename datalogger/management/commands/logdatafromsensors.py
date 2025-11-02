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



# from typing import Callable, Dict, Tuple
#
# from django.conf import settings
# from django.core.management.base import BaseCommand
#
# from m5stack import QMP6988, SHT30, QMP6988Fake, SHT30Fake
# from datalogger.models import Sensor, Measure
#
# # Extract constant: kódy senzorů
# SHT30_TEMP_CODE = "M5STACK-ENV-3-UNIT-SHT30-TEMPERATURE"
# SHT30_HUMIDITY_CODE = "M5STACK-ENV-3-UNIT-SHT30-HUMIDITY"
# QMP6988_PRESSURE_CODE = "M5STACK-ENV-3-UNIT-QMP6988-PRESSURE"
#
#
# class Command(BaseCommand):
#     help = "Načte měření z M5Stack ENV III (SHT30, QMP6988) a uloží je do Measure."
#
#     def _get_drivers(self) -> Tuple[QMP6988 | QMP6988Fake, SHT30 | SHT30Fake]:
#         """
#         Vybere reálné nebo falešné drivery podle settings.SENSORS_ENABLED.
#         """
#         if getattr(settings, "SENSORS_ENABLED", False):
#             return QMP6988(), SHT30()
#         return QMP6988Fake(), SHT30Fake()
#
#     def handle(self, *args, **options):
#         qmp6988, sht30 = self._get_drivers()
#
#         # Mapování kódu senzoru na funkci pro čtení hodnoty
#         readers: Dict[str, Callable[[], float]] = {
#             SHT30_TEMP_CODE: sht30.read_temperature,
#             SHT30_HUMIDITY_CODE: sht30.read_humidity,
#             QMP6988_PRESSURE_CODE: qmp6988.read_pressure,
#         }
#
#         # Načti pouze relevantní senzory a jen potřebná pole
#         sensors = Sensor.objects.filter(code__in=readers.keys()).only("id", "code")
#
#         # Vytvoř seznam měření bez duplicitní logiky if/if/if
#         measures_to_create = [
#             Measure(sensor=sensor, value=readers[sensor.code]())
#             for sensor in sensors
#         ]
#
#         if measures_to_create:
#             Measure.objects.bulk_create(measures_to_create)
