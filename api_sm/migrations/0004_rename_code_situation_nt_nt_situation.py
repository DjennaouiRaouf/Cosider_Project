# Generated by Django 4.2.7 on 2023-12-18 14:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_sm', '0003_rename_libelle_nt_libelle_nt_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='nt',
            old_name='code_situation_nt',
            new_name='situation',
        ),
    ]
