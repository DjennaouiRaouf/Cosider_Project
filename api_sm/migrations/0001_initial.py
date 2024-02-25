# Generated by Django 4.2.7 on 2024-02-25 14:19

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('api_sch', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('qte_precedente', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=38, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Quantité precedent')),
                ('qte_mois', models.DecimalField(decimal_places=2, default=0, max_digits=38, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Quantité Mois')),
                ('qte_cumule', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=38, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Quantité cumule')),
                ('prix_u', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=38, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Prix unitaire')),
                ('montant_precedent', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=38, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Montant précedent')),
                ('montant_mois', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=38, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Montant du Mois')),
                ('montant_cumule', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=38, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Montant cumulé')),
                ('date', models.DateField(verbose_name='Date')),
            ],
            options={
                'verbose_name': 'Attachements',
                'verbose_name_plural': 'Attachements',
            },
        ),
        migrations.CreateModel(
            name='Avance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('num_avance', models.PositiveIntegerField(blank=True, default=0, editable=False, verbose_name="Numero d'avance")),
                ('taux_avance', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=38, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name="Taux d'avance")),
                ('montant', models.DecimalField(decimal_places=2, default=0, max_digits=38, validators=[django.core.validators.MinValueValidator(0)], verbose_name="Montant d'avance")),
                ('fin', models.DecimalField(decimal_places=2, default=80, max_digits=38, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='% Fin')),
                ('date', models.DateField(verbose_name="Date d'avance")),
                ('remboursee', models.BooleanField(default=False, verbose_name='Est Remboursée')),
            ],
            options={
                'verbose_name': 'Avance',
                'verbose_name_plural': 'Avances',
            },
        ),
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('id', models.CharField(db_column='Code_Client', max_length=500, primary_key=True, serialize=False, verbose_name='Code du Client')),
                ('type_client', models.PositiveSmallIntegerField(blank=True, db_column='Type_Client', null=True, verbose_name='Type de Client')),
                ('est_client_cosider', models.BooleanField(blank=True, db_column='Est_Client_Cosider', verbose_name='Est Client Cosider')),
                ('libelle', models.CharField(blank=True, db_column='Libelle_Client', max_length=300, null=True, verbose_name='Libelle')),
                ('adresse', models.CharField(blank=True, db_column='adresse', max_length=500, null=True, verbose_name='Adresse')),
                ('nif', models.CharField(blank=True, db_column='NIF', max_length=50, null=True, unique=True, verbose_name='NIF')),
                ('raison_social', models.CharField(blank=True, db_column='Raison_Social', max_length=50, null=True, verbose_name='Raison Social')),
                ('num_registre_commerce', models.CharField(blank=True, db_column='Num_Registre_Commerce', max_length=20, null=True, verbose_name='Numero du registre de commerce')),
            ],
            options={
                'verbose_name': 'Clients',
                'verbose_name_plural': 'Clients',
            },
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('key', models.BigAutoField(primary_key=True, serialize=False)),
                ('src', models.ImageField(blank=True, default='default.png', upload_to='Images/Images')),
                ('type', models.CharField(blank=True, choices=[('H', 'Home'), ('L', 'Login')], max_length=100)),
            ],
            options={
                'verbose_name': 'Images',
                'verbose_name_plural': 'Images',
            },
        ),
        migrations.CreateModel(
            name='Marche',
            fields=[
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('id', models.CharField(max_length=500, primary_key=True, serialize=False, verbose_name='Code du Contrat')),
                ('libelle', models.CharField(max_length=500, verbose_name='Libelle')),
                ('ods_depart', models.DateField(blank=True, verbose_name='ODS de démarrage')),
                ('delais', models.PositiveIntegerField(default=0, verbose_name='Délai des travaux')),
                ('revisable', models.BooleanField(default=True, verbose_name='Est-il révisable ?')),
                ('delai_paiement_f', models.PositiveIntegerField(default=0, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Délai de paiement')),
                ('rabais', models.DecimalField(decimal_places=2, default=0, max_digits=38, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Taux de rabais')),
                ('tva', models.DecimalField(decimal_places=2, default=0, max_digits=38, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='TVA')),
                ('rg', models.DecimalField(decimal_places=2, default=0, max_digits=38, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Taux de retenue de garantie')),
                ('ht', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=38, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Montant Hors taxe')),
                ('ttc', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=38, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Montant avec taxe')),
                ('date_signature', models.DateField(verbose_name='Date de signature')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ModePaiement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('libelle', models.CharField(max_length=500, unique=True)),
            ],
            options={
                'verbose_name': 'Mode de Paiement',
                'verbose_name_plural': 'Mode de Paiement',
            },
        ),
        migrations.CreateModel(
            name='OptionImpression',
            fields=[
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('key', models.BigAutoField(primary_key=True, serialize=False)),
                ('src', models.ImageField(blank=True, upload_to='Images/Impression')),
                ('type', models.CharField(choices=[('H', 'Header'), ('F', 'Footer'), ('L', 'Logo')], max_length=20, unique=True)),
            ],
            options={
                'verbose_name': "Option d'Impression",
                'verbose_name_plural': "Option d'Impression",
            },
        ),
        migrations.CreateModel(
            name='Sites',
            fields=[
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('id', models.CharField(db_column='Code_site', max_length=500, primary_key=True, serialize=False, verbose_name='Code du Site')),
                ('responsable_site', models.CharField(blank=True, db_column='Responsable', max_length=500, null=True, verbose_name='Responsable du Site')),
                ('libelle', models.CharField(blank=True, db_column='Libelle_Site', max_length=500, null=True, verbose_name='Libelle du Site')),
                ('type_site', models.PositiveSmallIntegerField(blank=True, db_column='Type_Site', null=True, verbose_name='Type du Site')),
                ('code_filiale', models.CharField(blank=True, db_column='Code_Filiale', max_length=50, null=True, verbose_name='Code Filiale')),
                ('code_division', models.CharField(blank=True, db_column='Code_Division', max_length=50, null=True, verbose_name='Code division')),
                ('code_region', models.CharField(blank=True, db_column='Code_Region', max_length=20, null=True, verbose_name='Code région')),
                ('code_commune_site', models.CharField(blank=True, db_column='Code_Commune_Site', max_length=50, null=True, verbose_name='Code commune')),
                ('date_ouverture_site', models.DateField(blank=True, db_column='Date_Ouverture_Site', null=True, verbose_name='Ouverture')),
                ('date_cloture_site', models.DateField(blank=True, db_column='Date_Cloture_Site', null=True, verbose_name='Cloture')),
            ],
            options={
                'verbose_name': 'Sites',
                'verbose_name_plural': 'Sites',
            },
        ),
        migrations.CreateModel(
            name='SituationNt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('libelle', models.CharField(max_length=100, unique=True, verbose_name='Libelle')),
            ],
            options={
                'verbose_name': 'Situation du Travail',
                'verbose_name_plural': 'Situation du Travail',
            },
        ),
        migrations.CreateModel(
            name='TabUniteDeMesure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('libelle', models.CharField(blank=True, db_column='Symbole_Unite', max_length=10, null=True)),
                ('description', models.CharField(blank=True, db_column='Libelle_Unite', max_length=50, null=True)),
            ],
            options={
                'verbose_name': 'Unite de Mesure',
                'verbose_name_plural': 'Unite de Mesure',
                'db_table': 'Tab_Unite_de_Mesure',
            },
        ),
        migrations.CreateModel(
            name='TimeLine',
            fields=[
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('key', models.BigAutoField(primary_key=True, serialize=False)),
                ('year', models.PositiveIntegerField(blank=True, default=2024)),
                ('title', models.CharField(blank=True, max_length=100)),
                ('description', models.TextField(blank=True, max_length=300)),
            ],
            options={
                'verbose_name': 'TimeLine',
                'verbose_name_plural': 'TimeLine',
            },
        ),
        migrations.CreateModel(
            name='TypeAvance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('libelle', models.CharField(max_length=500, unique=True)),
                ('taux_max', models.DecimalField(decimal_places=2, default=0, max_digits=38, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
            ],
            options={
                'verbose_name': 'Type Avance',
                'verbose_name_plural': 'Type Avance',
            },
        ),
        migrations.CreateModel(
            name='TypeCaution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('libelle', models.CharField(blank=True, max_length=500, null=True)),
                ('taux_exact', models.DecimalField(blank=True, decimal_places=2, max_digits=38, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('taux_min', models.DecimalField(blank=True, decimal_places=2, max_digits=38, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('taux_max', models.DecimalField(blank=True, decimal_places=2, max_digits=38, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('type_avance', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api_sm.typeavance', verbose_name="Type d'avance")),
            ],
            options={
                'verbose_name': 'Type_Caution',
                'verbose_name_plural': 'Type_Caution',
            },
        ),
        migrations.CreateModel(
            name='Ordre_De_Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('date', models.DateField(blank=True, null=True, verbose_name='Date Interruption')),
                ('rep_int', models.CharField(choices=[('Interruption', 'Interruption'), ('Reprise', 'Interruption')], default='Interruption', max_length=300, verbose_name='Reprise/Interruption')),
                ('motif', models.TextField(blank=True, null=True, verbose_name='Motif')),
                ('marche', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='ods_marche', to='api_sm.marche')),
            ],
            options={
                'verbose_name': 'Ordre de service',
                'verbose_name_plural': 'Ordre de service',
            },
        ),
        migrations.CreateModel(
            name='NT',
            fields=[
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('id', models.CharField(db_column='id', editable=False, max_length=500, primary_key=True, serialize=False, verbose_name='id')),
                ('nt', models.CharField(db_column='NT', max_length=20, verbose_name='Numero du travail')),
                ('libelle', models.CharField(blank=True, db_column='Libelle_NT', max_length=900, null=True, verbose_name='Libelle')),
                ('date_ouverture_nt', models.DateField(blank=True, db_column='Date_Ouverture_NT', null=True, verbose_name='Ouverture')),
                ('date_cloture_nt', models.DateField(blank=True, db_column='Date_Cloture_NT', null=True, verbose_name='Cloture')),
                ('code_client', models.ForeignKey(db_column='Code_Client', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api_sm.clients', verbose_name='Code du client')),
                ('code_site', models.ForeignKey(db_column='Code_site', on_delete=django.db.models.deletion.DO_NOTHING, to='api_sm.sites', verbose_name='Code du Site')),
                ('code_situation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api_sm.situationnt', verbose_name='Situation')),
            ],
            options={
                'verbose_name': 'Numero du travail',
                'verbose_name_plural': 'Numero du travail',
                'unique_together': {('code_site', 'nt')},
            },
        ),
        migrations.AddField(
            model_name='marche',
            name='nt',
            field=models.ForeignKey(db_column='nt', on_delete=django.db.models.deletion.DO_NOTHING, to='api_sm.nt', verbose_name='Numero Travail'),
        ),
        migrations.CreateModel(
            name='Factures',
            fields=[
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('numero_facture', models.CharField(max_length=800, primary_key=True, serialize=False, verbose_name='Numero de facture')),
                ('num_situation', models.IntegerField(verbose_name='Numero de situation')),
                ('du', models.DateField(verbose_name='Du')),
                ('au', models.DateField(verbose_name='Au')),
                ('paye', models.BooleanField(default=False, editable=False)),
                ('date', models.DateTimeField(auto_now=True)),
                ('montant_precedent', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=38, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Montant Precedent')),
                ('montant_mois', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=38, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Montant du Mois')),
                ('montant_cumule', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=38, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Montant Cumulé')),
                ('montant_rb', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=38, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Montant du rabais')),
                ('montant_rg', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=38, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Montant Retenue de garantie')),
                ('montant_avf_remb', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=38, validators=[django.core.validators.MinValueValidator(0)], verbose_name="Montant d'avance forfaitaire remboursé")),
                ('montant_ava_remb', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=38, validators=[django.core.validators.MinValueValidator(0)], verbose_name="Montant d'avance appros remboursé")),
                ('montant_factureHT', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=38, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Montant de la facture HT')),
                ('montant_factureTTC', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=38, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Montant de la facture TTC')),
                ('taux_realise', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=38, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MinValueValidator(100)], verbose_name='Taux Realisé')),
                ('is_remb', models.BooleanField(default=False, editable=False, verbose_name='Remboursement Effectué')),
                ('marche', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api_sm.marche', verbose_name='Marche')),
            ],
            options={
                'verbose_name': 'Factures',
                'verbose_name_plural': 'Factures',
            },
        ),
        migrations.CreateModel(
            name='DQE',
            fields=[
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('id', models.CharField(db_column='id', editable=False, max_length=500, primary_key=True, serialize=False, verbose_name='id')),
                ('code_tache', models.CharField(db_column='Code_Tache', max_length=30, verbose_name='Code de la tache')),
                ('libelle', models.TextField(db_column='Libelle_Tache', verbose_name='Libelle')),
                ('prix_q', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=38, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Montant')),
                ('prix_u', models.DecimalField(decimal_places=2, default=0, max_digits=38, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Prix unitaire')),
                ('est_tache_composite', models.BooleanField(blank=True, db_column='Est_Tache_Composite', default=False, verbose_name='Tache composée')),
                ('est_tache_complementaire', models.BooleanField(blank=True, db_column='Est_Tache_Complementaire', default=False, verbose_name='Tache complementaire')),
                ('quantite', models.DecimalField(decimal_places=2, default=0, max_digits=38, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Quantité')),
                ('marche', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='marche_dqe', to='api_sm.marche', verbose_name='Code du marché')),
                ('unite', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api_sm.tabunitedemesure', verbose_name='Unité de mesure')),
            ],
            options={
                'verbose_name': 'DQE',
                'verbose_name_plural': 'DQE',
                'permissions': [('upload_dqe', 'Can upload DQE'), ('download_dqe', 'Can download DQE')],
            },
        ),
        migrations.CreateModel(
            name='DetailFacture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('detail', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api_sm.attachements')),
                ('facture', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api_sm.factures')),
            ],
            options={
                'verbose_name': 'Datails Facture',
                'verbose_name_plural': 'Details Facture',
            },
        ),
        migrations.CreateModel(
            name='Cautions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('date_soumission', models.DateField(verbose_name='Date dépot')),
                ('taux', models.DecimalField(decimal_places=2, default=0, max_digits=38, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('montant', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=38, validators=[django.core.validators.MinValueValidator(0)])),
                ('est_recupere', models.BooleanField(default=False, verbose_name='Est Recuperée')),
                ('agence', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='api_sch.tabagence')),
                ('avance', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api_sm.avance')),
                ('marche', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='Caution_Marche', to='api_sm.marche')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api_sm.typecaution')),
            ],
            options={
                'verbose_name': 'Caution',
                'verbose_name_plural': 'Caution',
            },
        ),
        migrations.AddField(
            model_name='avance',
            name='marche',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='Avance_Marche', to='api_sm.marche'),
        ),
        migrations.AddField(
            model_name='avance',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api_sm.typeavance', verbose_name="Type d'avance"),
        ),
        migrations.AddField(
            model_name='attachements',
            name='dqe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api_sm.dqe'),
        ),
        migrations.CreateModel(
            name='Remboursement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('montant_mois', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=38, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Montant Mois')),
                ('montant_cumule', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=38, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Montant Cumule')),
                ('rst_remb', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=38, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Reste à rembourser')),
                ('avance', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api_sm.avance')),
                ('facture', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api_sm.factures')),
            ],
            options={
                'verbose_name': 'Remboursement',
                'verbose_name_plural': 'Remboursements',
                'unique_together': {('facture', 'avance')},
            },
        ),
        migrations.CreateModel(
            name='Encaissement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('date_encaissement', models.DateField(verbose_name="Date d'encaissement")),
                ('montant_encaisse', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=38, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Montant encaissé')),
                ('montant_creance', models.DecimalField(blank=True, decimal_places=2, default=0, editable=False, max_digits=38, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Montant en créance')),
                ('numero_piece', models.CharField(max_length=300, verbose_name='Numero de piéce')),
                ('agence', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='api_sch.tabagence')),
                ('facture', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api_sm.factures', verbose_name='Facture')),
                ('mode_paiement', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api_sm.modepaiement', verbose_name='Mode de paiement')),
            ],
            options={
                'verbose_name': 'Encaissement',
                'verbose_name_plural': 'Encaissement',
                'unique_together': {('facture', 'date_encaissement')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='attachements',
            unique_together={('dqe', 'date')},
        ),
    ]
