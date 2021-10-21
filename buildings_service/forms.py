from django import forms
from django.core.validators import FileExtensionValidator

from . import models
from .constants import ChartTypes, UploadFileTypes


class UploadForm(forms.Form):
    """ A form for uploading the data CSV files """
    FILE_TYPES = [
        (UploadFileTypes.BUILDING_DATA, 'Building Data'),
        (UploadFileTypes.HALF_HOURLY_DATA, 'Half Hourly Data'),
        (UploadFileTypes.METER_DATA, 'Meter Data')
    ]
    upload_file = forms.FileField(
        error_messages={'required': 'Please select a file'},
        label='File',
        required=True,
        validators=[FileExtensionValidator(
            allowed_extensions=['csv']
        )]
    )
    file_type = forms.IntegerField(
        label='Type',
        required=True,
        widget=forms.Select(choices=FILE_TYPES)
    )
