# Generated by Django 5.1.7 on 2025-03-18 22:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tracker", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Trip",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start_lat", models.FloatField()),
                ("start_lng", models.FloatField()),
                ("end_lat", models.FloatField()),
                ("end_lng", models.FloatField()),
                ("distance", models.FloatField()),
                ("duration", models.FloatField()),
                ("average_speed", models.FloatField()),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
