# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class TabNtTaches(models.Model):
    code_site = models.OneToOneField('TabNt', models.DO_NOTHING, db_column='Code_site', primary_key=True)  # Field name made lowercase. The composite primary key (Code_site, NT, Code_Tache) found, that is not supported. The first column is selected.
    nt = models.ForeignKey('TabNt', models.DO_NOTHING, db_column='NT', to_field='NT', related_name='tabnttaches_nt_set')  # Field name made lowercase.
    code_tache = models.CharField(db_column='Code_Tache', max_length=30)  # Field name made lowercase.
    est_tache_composite = models.BooleanField(db_column='Est_Tache_Composite', blank=True, null=True)  # Field name made lowercase.
    est_tache_complementaire = models.BooleanField(db_column='Est_Tache_Complementaire', blank=True, null=True)  # Field name made lowercase.
    libelle_tache = models.TextField(db_column='Libelle_Tache', blank=True, null=True)  # Field name made lowercase.
    code_unite_mesure = models.ForeignKey('TabUniteDeMesure', models.DO_NOTHING, db_column='Code_Unite_Mesure', blank=True, null=True)  # Field name made lowercase.
    quantite = models.FloatField(db_column='Quantite', blank=True, null=True)  # Field name made lowercase.
    prix_unitaire = models.DecimalField(db_column='Prix_Unitaire', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    est_bloquer = models.BooleanField(db_column='Est_Bloquer', blank=True, null=True)  # Field name made lowercase.
    user_id = models.CharField(db_column='User_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    date_modification = models.DateTimeField(db_column='Date_Modification', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Tab_NT_Taches'
        unique_together = (('code_site', 'nt', 'code_tache'),)


class TabNt(models.Model):
    code_site = models.OneToOneField('TabSite', models.DO_NOTHING, db_column='Code_site', primary_key=True)  # Field name made lowercase. The composite primary key (Code_site, NT) found, that is not supported. The first column is selected.
    nt = models.CharField(db_column='NT', max_length=20)  # Field name made lowercase.
    code_client = models.ForeignKey('TabClient', models.DO_NOTHING, db_column='Code_Client')  # Field name made lowercase.
    code_situation_nt = models.ForeignKey('TabSituationNt', models.DO_NOTHING, db_column='Code_Situation_NT', blank=True, null=True)  # Field name made lowercase.
    libelle_nt = models.TextField(db_column='Libelle_NT', blank=True, null=True)  # Field name made lowercase.
    date_ouverture_nt = models.DateField(db_column='Date_Ouverture_NT', blank=True, null=True)  # Field name made lowercase.
    date_cloture_nt = models.DateField(db_column='Date_Cloture_NT', blank=True, null=True)  # Field name made lowercase.
    est_bloquer = models.BooleanField(db_column='Est_Bloquer', blank=True, null=True)  # Field name made lowercase.
    user_id = models.CharField(db_column='User_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    date_modification = models.DateTimeField(db_column='Date_Modification', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Tab_NT'
        unique_together = (('code_site', 'nt'),)


class TabUniteDeMesure(models.Model):
    code_unite_mesure = models.CharField(db_column='Code_Unite_Mesure', primary_key=True, max_length=4)  # Field name made lowercase.
    symbole_unite = models.CharField(db_column='Symbole_Unite', max_length=10, blank=True, null=True)  # Field name made lowercase.
    libelle_unite = models.CharField(db_column='Libelle_Unite', max_length=50, blank=True, null=True)  # Field name made lowercase.
    est_bloquer = models.BooleanField(db_column='Est_Bloquer', blank=True, null=True)  # Field name made lowercase.
    user_id = models.CharField(db_column='User_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    date_modification = models.DateTimeField(db_column='Date_Modification', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Tab_Unite_de_Mesure'


class TabSituationNt(models.Model):
    code_situation_nt = models.CharField(db_column='Code_Situation_NT', primary_key=True, max_length=2)  # Field name made lowercase.
    libelle_situation_nt = models.CharField(db_column='Libelle_Situation_NT', max_length=50, blank=True, null=True)  # Field name made lowercase.
    est_bloquer = models.BooleanField(db_column='Est_Bloquer', blank=True, null=True)  # Field name made lowercase.
    user_id = models.CharField(db_column='User_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    date_modification = models.DateTimeField(db_column='Date_Modification', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Tab_situation_NT'


class TabSite(models.Model):
    code_site = models.CharField(db_column='Code_site', primary_key=True, max_length=10)  # Field name made lowercase.
    code_filiale = models.ForeignKey('TabFiliale', models.DO_NOTHING, db_column='Code_Filiale')  # Field name made lowercase.
    code_region = models.CharField(db_column='Code_Region', max_length=1, blank=True, null=True)  # Field name made lowercase.
    libelle_site = models.CharField(db_column='Libelle_Site', max_length=150, blank=True, null=True)  # Field name made lowercase.
    code_agence = models.ForeignKey('TabAgence', models.DO_NOTHING, db_column='Code_Agence', blank=True, null=True)  # Field name made lowercase.
    type_site = models.SmallIntegerField(db_column='Type_Site', blank=True, null=True)  # Field name made lowercase.
    code_division = models.ForeignKey('TabDivision', models.DO_NOTHING, db_column='Code_Division', blank=True, null=True)  # Field name made lowercase.
    code_commune_site = models.CharField(db_column='Code_Commune_Site', max_length=10, blank=True, null=True)  # Field name made lowercase.
    jour_cloture_mouv_rh_paie = models.CharField(db_column='Jour_Cloture_Mouv_RH_Paie', max_length=2, blank=True, null=True)  # Field name made lowercase.
    date_ouverture_site = models.DateField(db_column='Date_Ouverture_Site', blank=True, null=True)  # Field name made lowercase.
    date_cloture_site = models.DateField(db_column='Date_Cloture_Site', blank=True, null=True)  # Field name made lowercase.
    est_bloquer = models.BooleanField(db_column='Est_Bloquer', blank=True, null=True)  # Field name made lowercase.
    user_id = models.CharField(db_column='User_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    date_modification = models.DateTimeField(db_column='Date_Modification', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Tab_Site'


class TabDivision(models.Model):
    code_division = models.CharField(db_column='Code_Division', primary_key=True, max_length=15)  # Field name made lowercase.
    code_filiale = models.ForeignKey('TabFiliale', models.DO_NOTHING, db_column='Code_Filiale', blank=True, null=True)  # Field name made lowercase.
    libelle_division = models.CharField(db_column='Libelle_Division', max_length=100, blank=True, null=True)  # Field name made lowercase.
    est_bloquer = models.BooleanField(db_column='Est_Bloquer', blank=True, null=True)  # Field name made lowercase.
    user_id = models.CharField(db_column='User_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    date_modification = models.DateTimeField(db_column='Date_Modification', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Tab_Division'





class TabFiliale(models.Model):
    code_filiale = models.CharField(db_column='Code_Filiale', primary_key=True, max_length=5)  # Field name made lowercase.
    code_entreprise = models.ForeignKey('TabEntreprise', models.DO_NOTHING, db_column='Code_Entreprise')  # Field name made lowercase.
    libelle_filiale = models.CharField(db_column='Libelle_Filiale', max_length=50, blank=True, null=True)  # Field name made lowercase.
    est_bloquer = models.BooleanField(db_column='Est_Bloquer', blank=True, null=True)  # Field name made lowercase.
    user_id = models.CharField(db_column='User_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    date_modification = models.DateTimeField(db_column='Date_Modification', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Tab_Filiale'


class TabEntreprise(models.Model):
    code_entreprise = models.CharField(db_column='Code_Entreprise', primary_key=True, max_length=2)  # Field name made lowercase.
    raison_social = models.CharField(db_column='Raison_Social', max_length=50, blank=True, null=True)  # Field name made lowercase.
    num_fiscal = models.CharField(db_column='Num_Fiscal', max_length=20, blank=True, null=True)  # Field name made lowercase.
    num_article = models.CharField(db_column='Num_Article', max_length=20, blank=True, null=True)  # Field name made lowercase.
    num_registre_commerce = models.CharField(db_column='Num_Registre_Commerce', max_length=20, blank=True, null=True)  # Field name made lowercase.
    num_compte = models.CharField(db_column='Num_Compte', max_length=20, blank=True, null=True)  # Field name made lowercase.
    capital = models.DecimalField(db_column='Capital', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    entete = models.TextField(db_column='Entete', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    date_registre_commerce = models.DateField(db_column='Date_Registre_Commerce', blank=True, null=True)  # Field name made lowercase.
    logo = models.BinaryField(db_column='Logo', blank=True, null=True)  # Field name made lowercase.
    type_dossier = models.SmallIntegerField(db_column='Type_Dossier')  # Field name made lowercase.
    est_bloquer = models.BooleanField(db_column='Est_Bloquer', blank=True, null=True)  # Field name made lowercase.
    user_id = models.CharField(db_column='User_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    date_modification = models.DateTimeField(db_column='Date_Modification', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Tab_Entreprise'
