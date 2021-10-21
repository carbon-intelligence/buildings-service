import graphene
from django.core.paginator import Paginator
from graphene_django.types import DjangoObjectType

from . import models


class PaginationMixin:
    page = graphene.Int()
    num_pages = graphene.Int()
    total_results = graphene.Int()


class Fuel(DjangoObjectType):
    class Meta:
        model = models.Fuel
        fields = ('id', 'unit', 'name')


class PaginatedFuels(PaginationMixin, graphene.ObjectType):
    results = graphene.List(Fuel)


class MeterReading(DjangoObjectType):
    class Meta:
        model = models.MeterReadings
        fields = ('id', 'meter', 'consumption', 'reading_date_time')


class PaginatedMeterReadings(PaginationMixin, graphene.ObjectType):
    results = graphene.List(MeterReading)


class Meter(DjangoObjectType):
    class Meta:
        model = models.Meter
        fields = ('id', 'building', 'fuel')

    fuel = graphene.Field(Fuel)
    meter_readings = graphene.List(MeterReading)

    def resolve_meter_readings(root, info):
        return models.MeterReadings.objects.filter(meter_id=root.id)


class PaginatedMeters(PaginationMixin, graphene.ObjectType):
    results = graphene.List(Meter)


class Building(DjangoObjectType):
    class Meta:
        model = models.Building
        fields = ('id', 'name')

    meters = graphene.List(Meter)

    def resolve_meters(root, info):
        return models.Meter.objects.filter(building_id=root.id)


class PaginatedBuildings(PaginationMixin, graphene.ObjectType):
    results = graphene.List(Building)


class Query(graphene.ObjectType):
    building = graphene.Field(Building, id=graphene.Int())
    buildings = graphene.Field(
        PaginatedBuildings,
        page=graphene.Int(required=True),
        page_size=graphene.Int(required=True)
    )
    fuel = graphene.Field(Fuel, id=graphene.Int())
    fuels = graphene.Field(
        PaginatedFuels,
        page=graphene.Int(required=True),
        page_size=graphene.Int(required=True)
    )
    meter = graphene.Field(Meter, id=graphene.Int())
    meters = graphene.Field(
        PaginatedMeters,
        page=graphene.Int(required=True),
        page_size=graphene.Int(required=True)
    )
    meter_reading = graphene.Field(MeterReading, id=graphene.Int())
    meter_readings = graphene.Field(
        PaginatedMeterReadings,
        page=graphene.Int(required=True),
        page_size=graphene.Int(required=True)
    )

    @classmethod
    def make_paginated_response(cls, qs, page, page_size):
        paginator = Paginator(qs, page_size)
        return {
            'results': paginator.page(page),
            'page': page,
            'num_pages': paginator.num_pages,
            'total_results': paginator.count
        }

    def resolve_building(root, info, id):
        return models.Building.objects.get(id=id)

    def resolve_buildings(root, info, page, page_size):
        qs = models.Building.objects.all()
        return Query.make_paginated_response(qs, page, page_size)

    def resolve_fuel(root, info, id):
        return models.Fuel.objects.get(id=id)

    def resolve_fuels(root, info, page, page_size):
        qs = models.Fuel.objects.all()
        return Query.make_paginated_response(qs, page, page_size)

    def resolve_meter(root, info, id):
        return models.Meter.objects.get(id=id)

    def resolve_meters(root, info, page, page_size):
        qs = models.Meter.objects.all()
        return Query.make_paginated_response(qs, page, page_size)

    def resolve_meter_reading(root, info, id):
        return models.MeterReadings.objects.get(id=id)

    def resolve_meter_readings(root, info, page, page_size):
        qs = models.MeterReadings.objects.all()
        return Query.make_paginated_response(qs, page, page_size)


schema = graphene.Schema(query=Query)
