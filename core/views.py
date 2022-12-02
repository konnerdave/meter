import matplotlib.pyplot as plot

from calendar import monthrange

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from matplotlib.backends.backend_agg import FigureCanvasAgg

from core.models import Building, Meter, MeterConsumption
from core.utils import get_csv_files


class CsvUploadView(TemplateView):
    """
    CSV Upload View
    """

    template_name = "index.html"

    def post(self, request, *args, **kwargs):
        files = {
            "building_data": request.FILES.get("building_data"),
            "halfhourly_data": request.FILES.get("halfhourly_data"),
            "meter_data": request.FILES.get("meter_data"),
        }

        if get_csv_files(files):
            building_data = Building.objects.all()
            meter_data = Meter.objects.all()
            meter_consumption_data = MeterConsumption.objects.all()

            context = {
                "building_data": building_data,
                "meter_data": meter_data,
                "meter_consumption_data": meter_consumption_data,
            }
            return render(request, "building.html", context)

        return render(request, "index.html")


class BuildingMeterView(TemplateView):
    """
    Building Meter View
    """

    template_name = "buildings_meter.html"

    def get(self, request, *args, **kwargs):
        building_id = kwargs.get("building_id")
        building_meters = Meter.objects.filter(building=building_id)

        context = {
            "meter_data": building_meters,
        }

        return render(request, self.template_name, context)


class MeterConsumptionView(TemplateView):
    """
    Building Meter Consumption View
    """

    template_name = "buildings_meter_consumption.html"

    def get(self, request, *args, **kwargs):
        meter_id = kwargs.get("meter_id")
        meter_consumption = MeterConsumption.objects.filter(meter_id=meter_id)

        context = {
            "meter_consumption_data": meter_consumption,
        }

        if meter_consumption.first():
            context["meter_id"] = meter_consumption.first().meter.id

        return render(request, self.template_name, context)


class MeterChartView(TemplateView):
    """
    Building Meter Consumption Chart View
    """

    template_name = "chart.html"
    MONTHS = [
        "January",
        "FebruaryFebruary",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]

    def get(self, request, *args, **kwargs):
        month_days = []
        month_consumption = []

        meter_id = kwargs.get("meter_id")
        meter_consumption = MeterConsumption.objects.filter(meter_id=meter_id).first()
        last_day = monthrange(
            meter_consumption.reading_at.year, meter_consumption.reading_at.month
        )[1]

        for day in range(1, last_day + 1):
            month_consumption.append(
                MeterConsumption.objects.filter(
                    meter_id=meter_id, reading_at__day=day
                ).aggregate(daily_consumption=Sum("consumption"))["daily_consumption"]
            )
            month_days.append(day)

        figure = plot.figure(figsize=(10, 5))
        axis = plot.gca()
        plot.xlabel("Days")
        plot.ylabel("Consumption (kWh)")
        plot.title(
            f"Daily Consumption For Month \
                {self.MONTHS[meter_consumption.reading_at.month - 1]}"
        )

        month_consumption = [0 if x is None else x for x in month_consumption]
        axis.bar(month_days, month_consumption)
        canvas = FigureCanvasAgg(figure)
        response = HttpResponse(content_type="image/png")
        canvas.print_png(response)
        return response
