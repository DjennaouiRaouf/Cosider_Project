# Generated by Django 4.2.7 on 2024-02-07 13:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_sm', '0003_factures_montan_avf_remb'),
    ]

    operations = [
        migrations.AddField(
            model_name='factures',
            name='montan_ava_remb',
            field=models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=38, validators=[django.core.validators.MinValueValidator(0)], verbose_name="Montant d'avance appros remboursé"),
        ),
    ]