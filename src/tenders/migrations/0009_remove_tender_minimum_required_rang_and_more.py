# Generated by Django 4.1.7 on 2023-04-12 21:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tenders", "0008_tender_minimum_required_rang"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="tender",
            name="minimum_required_rang",
        ),
        migrations.AddField(
            model_name="tender",
            name="minimum_required_rank",
            field=models.PositiveIntegerField(default=0),
        ),
    ]