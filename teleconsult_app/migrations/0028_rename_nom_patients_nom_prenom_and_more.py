# Generated by Django 5.1.2 on 2024-11-02 13:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teleconsult_app', '0027_rename_medecin_id_rendezvous_medecin_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='patients',
            old_name='nom',
            new_name='nom_prenom',
        ),
        migrations.RenameField(
            model_name='patients',
            old_name='prenom',
            new_name='username',
        ),
        migrations.RemoveField(
            model_name='patients',
            name='date_de_naissance',
        ),
    ]
