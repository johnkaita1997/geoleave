# Generated by Django 4.2.9 on 2024-01-19 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_holiday_holiday_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='holiday',
            name='dateofcreation',
        ),
        migrations.AlterField(
            model_name='holiday',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
