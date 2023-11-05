# Generated by Django 4.1 on 2023-11-05 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_sm', '0002_sites'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sites',
            name='date_modification',
            field=models.DateTimeField(auto_now=True, db_column='Date_Modification', null=True),
        ),
        migrations.AlterField(
            model_name='sites',
            name='est_bloquer',
            field=models.BooleanField(blank=True, db_column='Est_Bloquer', default=False, null=True),
        ),
    ]
