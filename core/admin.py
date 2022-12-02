from django.contrib import admin

from core.models import Building, Meter, MeterConsumption


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    pass


@admin.register(Meter)
class MeterAdmin(admin.ModelAdmin):
    pass


@admin.register(MeterConsumption)
class MeterConsumptionAdmin(admin.ModelAdmin):
    pass
