# Generated by Django 4.2.7 on 2024-02-13 09:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_sm', '0044_alter_remboursement_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='remboursement',
            name='facture',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api_sm.factures'),
        ),
    ]
