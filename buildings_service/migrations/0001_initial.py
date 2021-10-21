# Generated by Django 3.2.4 on 2021-10-21 10:11
import os
from django.db import migrations, models
import django.db.models.deletion
from ..services import csv_uploader
from ..constants import UploadFileTypes


def load_data(apps, schema_editor):
    for csv_name, file_type in [\
        ('building_data.csv', UploadFileTypes.BUILDING_DATA),
        ('meter_data.csv', UploadFileTypes.METER_DATA),
        ('halfhourly_data.csv', UploadFileTypes.HALF_HOURLY_DATA)
    ]:
        with open(f'{os.getcwd()}/buildings_service/test_data/{csv_name}', 'rb') as f:
            csv_uploader.upload(f, file_type=file_type)


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Fuel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit', models.CharField(choices=[('m3', 'm3'), ('kWh', 'kWh')], max_length=10)),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Meter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('building', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buildings_service.building')),
                ('fuel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buildings_service.fuel')),
            ],
        ),
        migrations.CreateModel(
            name='MeterReadings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consumption', models.DecimalField(decimal_places=5, max_digits=15)),
                ('reading_date_time', models.DateTimeField(db_index=True)),
                ('meter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buildings_service.meter')),
            ],
        ),
        migrations.RunPython(load_data)
    ]
