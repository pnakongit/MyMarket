# Generated by Django 4.1.7 on 2023-04-07 17:40

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tenders", "0002_alter_tender_end_day"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tender",
            name="end_day",
            field=models.DateField(default=datetime.date(2023, 4, 17)),
        ),
    ]