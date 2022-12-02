import pandas as pd

from .models import Building, Meter, MeterConsumption


def filter_building_data(building_file):
    # Filter building data from building CSV file.

    building_df = pd.DataFrame(building_file)
    # building_df_index = building_df.iloc[0].str.decode("utf-8")[0].split(',')[:2]

    for i in range(1, len(building_df)):
        data = building_df.iloc[i].str.decode("utf-8")[0].split(",")[:2]

        # CSV filter data
        id = data[0]
        name = data[1]

        if id != "":
            queryset = Building.objects.filter(id=id)

            if queryset.exists():
                queryset.update(name=name)
            else:
                Building.objects.create(id=id, name=name)


def filter_meter_data(meter_file):
    # Filter meter data from meter CSV file.

    meter_df = pd.DataFrame(meter_file)
    # meter_df_index = meter_df.iloc[0].str.decode("utf-8")[0].split(',')

    for i in range(1, len(meter_df)):
        data = meter_df.iloc[i].str.decode("utf-8")[0].split(",")

        # CSV filter data
        building_id = data[0]
        id = data[1]
        fuel_type = data[2]
        unit = data[3].strip()

        if id != "":
            queryset = Meter.objects.filter(id=id)

            if queryset.exists():
                queryset.update(
                    building_id=building_id,
                    fuel_type=fuel_type,
                    unit=unit
                )
            else:
                Meter.objects.create(
                    bbuilding_id=building_id,
                    id=id,
                    fuel_type=fuel_type,
                    unit=unit
                )


def filter_halfhourly_data(halfhourly_file):
    # Filter halfhourly data from halfhourly CSV file.

    halfhourly_df = pd.DataFrame(halfhourly_file).head()
    # halfhourly_df_index = halfhourly_df.iloc[0].str.decode("utf-8")[0].split(',')

    for i in range(1, len(halfhourly_df)):
        data = halfhourly_df.iloc[i].str.decode("utf-8")[0].split(",")

        # CSV filter data
        consumption = data[0]
        meter_id = data[1]
        reading_at = data[2].strip()

        if consumption != "":
            MeterConsumption.objects.create(
                consumption=consumption,
                meter_id=meter_id,
                reading_at=reading_at
            )


def get_csv_files(files):
    try:
        building_file = files.get("building_data")
        meter_file = files.get("meter_data")
        halfhourly_file = files.get("halfhourly_data")

        filter_building_data(building_file)
        filter_meter_data(meter_file)
        filter_halfhourly_data(halfhourly_file)

        return True
    except Exception:
        return False
