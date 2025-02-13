# Generated by Django 5.1.6 on 2025-02-13 13:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_alter_developer_skills"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Project",
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
                ("project_name", models.CharField(max_length=50)),
                ("description", models.TextField(blank=True)),
                ("maximum_collaborators", models.IntegerField()),
                (
                    "collaborators",
                    models.ManyToManyField(
                        blank=True,
                        related_name="collaborators",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "owner",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="owner",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
