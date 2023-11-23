# Generated by Django 3.2.23 on 2023-11-23 12:19

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_currentuser.db.models.fields
import django_currentuser.middleware
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Avance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('montant', models.DecimalField(decimal_places=2, default=0, max_digits=38, validators=[django.core.validators.MinValueValidator(0)])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Banque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('nom', models.CharField(max_length=300)),
                ('adresse', models.CharField(max_length=300)),
                ('ville', models.CharField(max_length=300)),
                ('wilaya', models.CharField(max_length=300)),
                ('user_id', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Banque',
                'verbose_name_plural': 'Banque',
            },
        ),
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('code_client', models.CharField(db_column='Code_Client', max_length=500, primary_key=True, serialize=False)),
                ('type_client', models.PositiveSmallIntegerField(blank=True, db_column='Type_Client', null=True)),
                ('est_client_cosider', models.BooleanField(blank=True, db_column='Est_Client_Cosider')),
                ('libelle_client', models.CharField(blank=True, db_column='Libelle_Client', max_length=300, null=True)),
                ('nif', models.CharField(blank=True, db_column='NIF', max_length=50, null=True, unique=True)),
                ('raison_social', models.CharField(blank=True, db_column='Raison_Social', max_length=50, null=True)),
                ('num_registre_commerce', models.CharField(blank=True, db_column='Num_Registre_Commerce', max_length=20, null=True)),
                ('date_modification', models.DateTimeField(auto_now=True, db_column='Date_Modification')),
                ('user_id', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
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
                ('src', models.ImageField(blank=True, default='default.png', upload_to='Images/Login')),
                ('est_bloquer', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Images',
                'verbose_name_plural': 'Images',
            },
        ),
        migrations.CreateModel(
            name='Marche',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('num_avenant', models.PositiveBigIntegerField(default=0, editable=False)),
                ('nbr_avenant', models.PositiveBigIntegerField(default=0, editable=False)),
                ('libelle', models.CharField(blank=True, max_length=500)),
                ('ods_depart', models.DateField(blank=True)),
                ('delais', models.PositiveIntegerField(default=0)),
                ('revisable', models.BooleanField(default=True)),
                ('rabais', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('tva', models.DecimalField(decimal_places=2, default=0, max_digits=38, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('retenue_de_garantie', models.DecimalField(decimal_places=2, default=0, max_digits=38, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('code_contrat', models.CharField(blank=True, max_length=20)),
                ('date_signature', models.DateTimeField(auto_now=True, db_column='Date_Signature')),
                ('avenant_du_contrat', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='avenants', to='api_sm.marche')),
            ],
            options={
                'verbose_name': 'Marchés',
                'verbose_name_plural': 'Marchés',
            },
        ),
        migrations.CreateModel(
            name='TypeCaution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('libelle', models.CharField(max_length=500)),
                ('taux', models.DecimalField(decimal_places=2, default=0, max_digits=38, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('user_id', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Type_Caution',
                'verbose_name_plural': 'Type_Caution',
            },
        ),
        migrations.CreateModel(
            name='TypeAvance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('libelle', models.CharField(max_length=500, unique=True)),
                ('user_id', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Type Avance',
                'verbose_name_plural': 'Type Avance',
            },
        ),
        migrations.CreateModel(
            name='Sites',
            fields=[
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('code_site', models.CharField(db_column='Code_site', max_length=10, primary_key=True, serialize=False)),
                ('code_filiale', models.CharField(db_column='Code_Filiale', max_length=5)),
                ('code_region', models.CharField(blank=True, db_column='Code_Region', max_length=1, null=True)),
                ('libelle_site', models.CharField(blank=True, db_column='Libelle_Site', max_length=150, null=True)),
                ('code_agence', models.CharField(blank=True, db_column='Code_Agence', max_length=15, null=True)),
                ('type_site', models.PositiveSmallIntegerField(blank=True, db_column='Type_Site', null=True)),
                ('code_division', models.CharField(blank=True, db_column='Code_Division', max_length=15, null=True)),
                ('code_commune_site', models.CharField(blank=True, db_column='Code_Commune_Site', max_length=10, null=True)),
                ('jour_cloture_mouv_rh_paie', models.CharField(blank=True, db_column='Jour_Cloture_Mouv_RH_Paie', max_length=2, null=True)),
                ('date_ouverture_site', models.DateField(blank=True, db_column='Date_Ouverture_Site')),
                ('date_cloture_site', models.DateField(blank=True, db_column='Date_Cloture_Site', null=True)),
                ('user_id', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Sites',
                'verbose_name_plural': 'Sites',
            },
        ),
        migrations.CreateModel(
            name='Ordre_De_Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('date_interruption', models.DateField(blank=True)),
                ('date_reprise', models.DateField(blank=True)),
                ('motif', models.TextField(blank=True)),
                ('marche', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ods_marche', to='api_sm.marche')),
                ('user_id', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Ordre de service',
                'verbose_name_plural': 'Ordre de service',
            },
        ),
        migrations.CreateModel(
            name='NT',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('nt', models.CharField(db_column='NT', max_length=20)),
                ('libelle_nt', models.TextField(blank=True, db_column='Libelle_NT', null=True)),
                ('date_ouverture_nt', models.DateField(blank=True, db_column='Date_Ouverture_NT', null=True)),
                ('date_cloture_nt', models.DateField(blank=True, db_column='Date_Cloture_NT', null=True)),
                ('code_client', models.ForeignKey(db_column='Code_Client', on_delete=django.db.models.deletion.CASCADE, to='api_sm.clients')),
                ('code_site', models.ForeignKey(db_column='Code_site', on_delete=django.db.models.deletion.CASCADE, to='api_sm.sites')),
                ('user_id', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
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
            field=models.ForeignKey(db_column='numero_marche', on_delete=django.db.models.deletion.CASCADE, to='api_sm.nt'),
        ),
        migrations.AddField(
            model_name='marche',
            name='user_id',
            field=django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='HistoricalDQE',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('designation', models.CharField(max_length=600)),
                ('unite', models.CharField(max_length=5)),
                ('prix_u', models.DecimalField(decimal_places=2, default=0, max_digits=38, validators=[django.core.validators.MinValueValidator(0)])),
                ('quantite', models.DecimalField(decimal_places=2, default=0, max_digits=38, validators=[django.core.validators.MinValueValidator(0)])),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('marche', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='api_sm.marche')),
            ],
            options={
                'verbose_name': 'historical DQE',
                'verbose_name_plural': 'historical DQE',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Factures',
            fields=[
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('numero_facture', models.CharField(max_length=500, primary_key=True, serialize=False)),
                ('date_facture', models.DateField(auto_now=True)),
                ('payer', models.BooleanField(default=False)),
                ('annulation', models.BooleanField(default=False)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_sm.clients')),
            ],
            options={
                'verbose_name': 'Factures',
                'verbose_name_plural': 'Factures',
            },
        ),
        migrations.CreateModel(
            name='DQE',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('designation', models.CharField(max_length=600)),
                ('unite', models.CharField(max_length=5)),
                ('prix_u', models.DecimalField(decimal_places=2, default=0, max_digits=38, validators=[django.core.validators.MinValueValidator(0)])),
                ('quantite', models.DecimalField(decimal_places=2, default=0, max_digits=38, validators=[django.core.validators.MinValueValidator(0)])),
                ('marche', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_sm.marche')),
            ],
            options={
                'verbose_name': 'DQE',
                'verbose_name_plural': 'DQE',
                'unique_together': {('marche', 'designation')},
            },
        ),
        migrations.CreateModel(
            name='Cautions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('date_soumission', models.DateField(blank=True)),
                ('montant', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=38, validators=[django.core.validators.MinValueValidator(0)])),
                ('est_recupere', models.BooleanField(default=True, editable=False)),
                ('avance', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api_sm.avance')),
                ('banque', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_sm.banque')),
                ('marche', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Caution_Marche', to='api_sm.marche')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_sm.typecaution')),
                ('user_id', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Caution',
                'verbose_name_plural': 'Caution',
            },
        ),
        migrations.AddField(
            model_name='avance',
            name='Client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Avance_Client', to='api_sm.marche'),
        ),
        migrations.AddField(
            model_name='avance',
            name='marche',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Avance_Marche', to='api_sm.marche'),
        ),
        migrations.AddField(
            model_name='avance',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_sm.typeavance'),
        ),
        migrations.AddField(
            model_name='avance',
            name='user_id',
            field=django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Attachements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('qte_realise', models.DecimalField(decimal_places=2, default=0, max_digits=38, validators=[django.core.validators.MinValueValidator(0)])),
                ('qte_restante', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=38, validators=[django.core.validators.MinValueValidator(0)])),
                ('dqe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_sm.dqe')),
                ('user_id', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Attachements',
                'verbose_name_plural': 'Attachements',
            },
        ),
        migrations.AlterUniqueTogether(
            name='marche',
            unique_together={('nt', 'num_avenant')},
        ),
        migrations.CreateModel(
            name='Encaissement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('date_encaissement', models.DateField()),
                ('mode_paiement', models.CharField(max_length=100)),
                ('montant_encaisse', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=38, validators=[django.core.validators.MinValueValidator(0)])),
                ('montant_creance', models.DecimalField(blank=True, decimal_places=2, default=0, editable=False, max_digits=38, validators=[django.core.validators.MinValueValidator(0)])),
                ('numero_piece', models.CharField(max_length=300)),
                ('banque', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_sm.banque')),
                ('facture', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='api_sm.factures')),
            ],
            options={
                'verbose_name': 'Encaissement',
                'verbose_name_plural': 'Encaissement',
                'unique_together': {('facture', 'date_encaissement')},
            },
        ),
        migrations.CreateModel(
            name='DetailFacture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_sm.attachements')),
                ('facture', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='api_sm.factures')),
            ],
            options={
                'verbose_name': 'Datails Facture',
                'verbose_name_plural': 'Details Facture',
                'unique_together': {('facture', 'detail')},
            },
        ),
    ]
