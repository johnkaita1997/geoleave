# Generated by Django 4.2.9 on 2024-01-08 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave_applications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaveapplication',
            name='is_actedon',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]