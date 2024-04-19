# Generated by Django 5.0.4 on 2024-04-19 10:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Author",
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
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Book",
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
                ("isbn", models.CharField(max_length=13, unique=True)),
                ("title", models.TextField()),
                (
                    "language_code",
                    models.CharField(db_index=True, max_length=35, null=True),
                ),
                (
                    "original_publication_year",
                    models.SmallIntegerField(db_index=True, null=True),
                ),
                (
                    "avg_borrowing_time",
                    models.PositiveIntegerField(
                        db_index=True, default=0, help_text="In days"
                    ),
                ),
                (
                    "borrowing_count",
                    models.PositiveIntegerField(db_index=True, default=0),
                ),
                ("is_available", models.BooleanField(db_index=True, default=True)),
                ("authors", models.ManyToManyField(to="library.author")),
            ],
        ),
        migrations.CreateModel(
            name="Borrowing",
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
                ("borrow_dt", models.DateTimeField()),
                ("return_dt", models.DateTimeField(null=True)),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="library.book"
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="borrowing",
            constraint=models.CheckConstraint(
                check=models.Q(("return_dt__gte", models.F("borrow_dt"))),
                name="return_dt_gte_borrow_dt",
            ),
        ),
    ]
