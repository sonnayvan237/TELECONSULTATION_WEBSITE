# Generated by Django 5.1.2 on 2024-11-05 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teleconsult_app', '0041_ordonnances'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordonnances',
            name='commentaire',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ordonnances',
            name='fichier',
            field=models.FileField(upload_to='ordonnances/'),
        ),
    ]
