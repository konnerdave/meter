from common.enums import ChoiceEnum


class FuelType(ChoiceEnum):
    WATER = 'Water'
    NATURAL_GAS = 'Natural Gas'
    ELECTRICITY = 'Electricity'


class UnitType(ChoiceEnum):
    KWH = 'kWh'
    M3 = 'm3'
