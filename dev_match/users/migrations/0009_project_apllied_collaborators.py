# Generated by Django 5.1.6 on 2025-02-13 15:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0008_alter_project_owner"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="apllied_collaborators",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="apllied_collaborators",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
