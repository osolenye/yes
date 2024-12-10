# Generated by Django 5.1.3 on 2024-12-10 20:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0004_remove_day_worked_day_span"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="leaverequest",
            name="full_name",
        ),
        migrations.AddField(
            model_name="leaverequest",
            name="worker",
            field=models.ForeignKey(
                default=1, on_delete=django.db.models.deletion.CASCADE, to="api.worker"
            ),
            preserve_default=False,
        ),
    ]