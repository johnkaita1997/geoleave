# Generated by Django 4.2.9 on 2024-01-19 11:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('leave_types', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Leaveapplication',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('dateofcreation', models.DateField(auto_now_add=True, null=True)),
                ('duration_in_days', models.IntegerField(blank=True, null=True)),
                ('expected_start_date', models.DateField(default='2020-12-12')),
                ('expected_end_date', models.DateField(default='2020-12-12')),
                ('is_cleared', models.BooleanField(blank=True, default=False, null=True)),
                ('clearance_date', models.DateField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('is_approved', models.BooleanField(blank=True, default=False, null=True)),
                ('is_active', models.BooleanField(blank=True, default=True, null=True)),
                ('is_actedon', models.BooleanField(blank=True, default=False, null=True)),
                ('approval_date', models.DateField(blank=True, null=True)),
                ('start_of_holiday_date', models.DateField(blank=True, null=True)),
                ('end_of_holiday_date', models.DateField(blank=True, null=True)),
                ('is_forwarded', models.BooleanField(blank=True, default=False, null=True)),
                ('forwarded_date', models.DateField(blank=True, null=True)),
                ('approval_user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='leave_applications_approval', to=settings.AUTH_USER_MODEL)),
                ('appuser', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='leave_applications', to=settings.AUTH_USER_MODEL)),
                ('leave', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='leave_applications', to='leave_types.leavetype')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
