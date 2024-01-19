# Generated by Django 4.2.9 on 2024-01-19 11:31

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Leavetype',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('dateofcreation', models.DateField(auto_now_add=True, null=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(blank=True, max_length=19255, null=True)),
                ('is_full_time_employee', models.BooleanField(default=False)),
                ('leave_duration_in_days', models.IntegerField(blank=True, default=3, null=True)),
                ('length_of_service_months', models.IntegerField(blank=True, default=3, null=True)),
                ('is_document_backed', models.BooleanField(default=False)),
                ('is_satisfactory_performance_based', models.BooleanField(default=False)),
                ('has_exhausted_normal_leave_days', models.BooleanField(default=False)),
                ('duration_is_request_basis', models.BooleanField(default=False)),
                ('is_paid', models.BooleanField(default=True)),
                ('is_compensatory', models.BooleanField(default=False)),
                ('is_normal', models.BooleanField(default=False)),
                ('days_in_advance', models.IntegerField(blank=True, default=3, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
