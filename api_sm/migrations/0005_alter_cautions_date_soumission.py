# Generated by Django 4.2.7 on 2024-01-22 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_sm', '0004_rename_banque_cautions_agence'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cautions',
            name='date_soumission',
            field=models.DateField(verbose_name='Date dépot'),
        ),
    ]
