# Generated by Django 5.1.2 on 2024-11-11 12:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teleconsult_app', '0049_rendezvous_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rendezvous',
            name='user',
        ),
    ]
