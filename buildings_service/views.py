from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.decorators.http import require_GET
from django.views.generic.list import ListView
from rest_framework import mixins, viewsets

from .services import csv_uploader
from . import forms, models, serializers


@require_GET
def index(request):
    """ Basic entry page for the site """
    return render(request, 'buildings_service/index.html')


class UploadView(View):
    """ View to upload data from csvs. Accepts GET and POST requests. """
    form = forms.UploadForm
    template = 'buildings_service/upload.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template, {'form': self.form()})

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST, request.FILES)
        if form.is_valid():
            csv_uploader.upload(
                request.FILES['upload_file'], form.cleaned_data['file_type'])

        return render(request, self.template, {'form': form})


class BuildingList(ListView):
    """ View for the list of all Buildings """
    model = models.Building
    context_object_name = 'buildings'


class MeterList(ListView):
    """
    View for the list of meters for a given building.
    Returns 404 if the Building cannot be found.
    """
    model = models.Meter
    context_object_name = 'meters'
    def get_queryset(self):
        self.building = get_object_or_404(models.Building, pk=self.kwargs['building_id'])
        return models.Meter.objects.filter(building=self.building).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['building'] = self.building
        return context


class MeterReadingsList(ListView):
    """
    View the list of meter readings for a given meter.
    Returns 404 if the Meter cannot be found.
    """
    model = models.MeterReadings
    context_object_name = 'meter_readings'

    def get_queryset(self):
        self.meter = get_object_or_404(models.Meter, pk=self.kwargs['meter_id'])
        return models.MeterReadings.objects.filter(meter=self.meter).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meter'] = self.meter
        return context


class BuildingViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = models.Building.objects.all()
    serializer_class = serializers.BuildingSerializer


class FuelViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = models.Fuel.objects.all()
    serializer_class = serializers.FuelSerializer


class MeterViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = models.Meter.objects.all()
    serializer_class = serializers.MeterSerializer


class MeterReadingViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = models.MeterReadings.objects.all()
    serializer_class = serializers.MeterReadingsSerializer
