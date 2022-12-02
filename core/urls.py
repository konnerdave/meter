from django.urls import path

from .views import (
    CsvUploadView,
    BuildingMeterView,
    MeterConsumptionView,
    MeterChartView,
)


urlpatterns = [
    path('', CsvUploadView.as_view(), name='CsvUpload'),
    path(
        'building_meter/<int:building_id>',
        BuildingMeterView.as_view(),
        name='building_meter',
    ),
    path(
        'meter_consumption/<int:meter_id>',
        MeterConsumptionView.as_view(),
        name='meter_consumption',
    ),
    path('meter_chart/<int:meter_id>', MeterChartView.as_view(), name='meter_chart'),
]
