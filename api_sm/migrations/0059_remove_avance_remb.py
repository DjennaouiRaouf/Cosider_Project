# Generated by Django 4.2.7 on 2024-02-19 09:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_sm', '0058_remove_avance_debut'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='avance',
            name='remb',
        ),
    ]
