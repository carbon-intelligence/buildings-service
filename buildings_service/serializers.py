from rest_framework import serializers
from . import models


class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.Building


class FuelSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.Fuel


class MeterSerializer(serializers.ModelSerializer):
    fuel = FuelSerializer

    class Meta:
        fields = '__all__'
        model = models.Meter


class MeterReadingsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.MeterReadings
