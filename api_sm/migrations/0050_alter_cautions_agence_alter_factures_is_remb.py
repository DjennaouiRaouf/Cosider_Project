# Generated by Django 4.2.7 on 2024-02-15 12:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_sch', '0002_alter_tabproduction_options'),
        ('api_sm', '0049_factures_is_remb'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cautions',
            name='agence',
            field=models.ForeignKey(db_column='Code_Agence', db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='api_sch.tabagence'),
        ),
        migrations.AlterField(
            model_name='factures',
            name='is_remb',
            field=models.BooleanField(default=False, editable=False, verbose_name='Remboursement Effectué'),
        ),
    ]
