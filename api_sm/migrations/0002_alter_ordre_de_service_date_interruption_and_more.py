# Generated by Django 4.2.7 on 2024-01-25 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_sm', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordre_de_service',
            name='date_interruption',
            field=models.DateField(blank=True, null=True, verbose_name='Date Interruption'),
        ),
        migrations.AlterField(
            model_name='ordre_de_service',
            name='date_reprise',
            field=models.DateField(blank=True, null=True, verbose_name='Date Reprise'),
        ),
        migrations.AlterField(
            model_name='ordre_de_service',
            name='motif',
            field=models.TextField(blank=True, verbose_name='Motif'),
        ),
    ]
