# Generated by Django 4.1.7 on 2023-04-12 21:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tenders", "0007_remove_tender_start_day_request_tender_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="tender",
            name="minimum_required_rang",
            field=models.PositiveIntegerField(default=0),
        ),
    ]