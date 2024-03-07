# Generated by Django 4.2.6 on 2024-03-07 16:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("cities_light", "0011_alter_city_country_alter_city_region_and_more"),
        ("Admin_app", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Employer",
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
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Hiring",
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
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                (
                    "hire_posting",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("is_hired", models.BooleanField(default=False)),
                ("cost", models.IntegerField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Pending", "Pending"),
                            ("Accepted", "Accepted"),
                            ("Rejected", "Rejected"),
                        ],
                        default="Pending",
                        max_length=10,
                    ),
                ),
                (
                    "employer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="NativeApp.employer",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="HiringHistory",
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
                ("employer_name", models.CharField(max_length=255)),
                ("worker_name", models.CharField(max_length=255)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("cost", models.IntegerField()),
                ("status", models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name="Worker",
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
                (
                    "availability",
                    models.JSONField(
                        default={
                            "Friday": True,
                            "Monday": True,
                            "Saturday": True,
                            "Sunday": True,
                            "Thursday": True,
                            "Tuesday": True,
                            "Wednesday": True,
                        }
                    ),
                ),
                ("wage", models.FloatField(null=True)),
                ("experience", models.FloatField(null=True)),
                (
                    "city",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="cities_light.city",
                    ),
                ),
                (
                    "country",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="cities_light.country",
                    ),
                ),
                (
                    "hiring_requests",
                    models.ManyToManyField(
                        related_name="workers", to="NativeApp.hiring"
                    ),
                ),
                (
                    "job_types",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Admin_app.typeofjobs",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="RejectionReason",
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
                ("reason_text", models.TextField()),
                (
                    "hiring",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="NativeApp.hiring",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Notification",
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
                ("messages", models.TextField()),
                ("is_read", models.BooleanField(default=False)),
                (
                    "hiring",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="NativeApp.hiring",
                    ),
                ),
                (
                    "worker",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="NativeApp.worker",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="hiring",
            name="worker",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="NativeApp.worker"
            ),
        ),
        migrations.CreateModel(
            name="Customer",
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
                ("phone_no", models.CharField(max_length=10)),
                ("profile_pic", models.ImageField(blank=True, upload_to="pics")),
                ("location", models.TextField(max_length=250)),
                (
                    "user_type",
                    models.CharField(
                        choices=[("employer", "employer"), ("worker", "worker")],
                        max_length=8,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
