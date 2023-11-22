# Generated by Django 3.2.23 on 2023-11-22 14:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_sm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='attachements',
            name='qte_restante',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=38, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
