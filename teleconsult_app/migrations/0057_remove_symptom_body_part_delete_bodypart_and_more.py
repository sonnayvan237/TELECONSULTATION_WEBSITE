# Generated by Django 5.1.6 on 2025-02-08 11:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("teleconsult_app", "0056_bodypart_symptom"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="symptom",
            name="body_part",
        ),
        migrations.DeleteModel(
            name="BodyPart",
        ),
        migrations.DeleteModel(
            name="Symptom",
        ),
    ]
