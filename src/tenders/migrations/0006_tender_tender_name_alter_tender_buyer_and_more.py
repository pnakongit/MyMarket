# Generated by Django 4.1.7 on 2023-04-12 09:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
        ("tenders", "0005_tender_start_day_alter_tender_end_day_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="tender",
            name="tender_name",
            field=models.CharField(default="", max_length=200),
        ),
        migrations.AlterField(
            model_name="tender",
            name="buyer",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tender",
                to="accounts.buyerprofile",
            ),
        ),
        migrations.AlterField(
            model_name="tender",
            name="description",
            field=models.TextField(default="", max_length=500),
        ),
    ]
