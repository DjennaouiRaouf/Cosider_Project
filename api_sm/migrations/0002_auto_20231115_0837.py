# Generated by Django 3.2.23 on 2023-11-15 07:37

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_sm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='marche',
            name='ht',
            field=models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=38, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='marche',
            name='ttc',
            field=models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=38, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.CreateModel(
            name='Factures',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_facture', models.CharField(max_length=500)),
                ('date_facture', models.DateField(blank=True)),
                ('montant', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=38, validators=[django.core.validators.MinValueValidator(0)])),
                ('montant_apres_rabais', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=38, validators=[django.core.validators.MinValueValidator(0)])),
                ('Attachements', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api_sm.attachements')),
            ],
        ),
    ]
