# Generated by Django 5.1.2 on 2024-11-01 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teleconsult_app', '0012_patients'),
    ]

    operations = [
        migrations.AddField(
            model_name='patients',
            name='age',
            field=models.IntegerField(default=True),
        ),
    ]
