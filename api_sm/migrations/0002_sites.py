# Generated by Django 4.1 on 2023-11-01 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_sm', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sites',
            fields=[
                ('code_site', models.CharField(db_column='Code_site', max_length=10, primary_key=True, serialize=False)),
                ('code_filiale', models.CharField(db_column='Code_Filiale', max_length=5)),
                ('code_region', models.CharField(blank=True, db_column='Code_Region', max_length=1, null=True)),
                ('libelle_site', models.CharField(blank=True, db_column='Libelle_Site', max_length=150, null=True)),
                ('code_agence', models.CharField(blank=True, db_column='Code_Agence', max_length=15, null=True)),
                ('type_site', models.SmallIntegerField(blank=True, db_column='Type_Site', null=True)),
                ('code_division', models.CharField(blank=True, db_column='Code_Division', max_length=15, null=True)),
                ('code_commune_site', models.CharField(blank=True, db_column='Code_Commune_Site', max_length=10, null=True)),
                ('jour_cloture_mouv_rh_paie', models.CharField(blank=True, db_column='Jour_Cloture_Mouv_RH_Paie', max_length=2, null=True)),
                ('date_ouverture_site', models.DateField(blank=True, db_column='Date_Ouverture_Site', null=True)),
                ('date_cloture_site', models.DateField(blank=True, db_column='Date_Cloture_Site', null=True)),
                ('est_bloquer', models.BooleanField(blank=True, db_column='Est_Bloquer', null=True)),
                ('user_id', models.CharField(blank=True, db_column='User_ID', max_length=15, null=True)),
                ('date_modification', models.DateTimeField(blank=True, db_column='Date_Modification', null=True)),
            ],
            options={
                'verbose_name': 'Sites',
                'verbose_name_plural': 'Sites',
            },
        ),
    ]
