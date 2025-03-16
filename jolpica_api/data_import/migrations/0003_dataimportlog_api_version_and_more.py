# Generated by Django 5.1.7 on 2025-03-16 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "data_import",
            "0002_rename_updated_records_dataimportlog_import_result_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="dataimportlog",
            name="api_version",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="dataimportlog",
            name="error_type",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="dataimportlog",
            name="errors",
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="dataimportlog",
            name="import_result",
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="dataimportlog",
            name="total_records",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
