from django.db import models

from core.enums import FuelType, UnitType


class Building(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Meter(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    fuel_type = models.CharField(
        max_length=128,
        choices=FuelType.choices(),
        default=FuelType.default(),
    )
    unit = models.CharField(
        max_length=128,
        choices=UnitType.choices(),
        default=UnitType.default(),
    )

    def __str__(self):
        return f'Meter #{self.pk}'


class MeterConsumption(models.Model):
    meter = models.ForeignKey(Meter, on_delete=models.CASCADE)
    consumption = models.FloatField()
    reading_at = models.DateTimeField()

    def __str__(self):
        return f'{self.meter}'
