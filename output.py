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
        db_table = 'Tab_NT_taches'
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
        db_table = 'tab_nt'
        unique_together = (('code_site', 'nt'),)


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
        db_table = 'tab_site'


class TabUniteDeMesure(models.Model):
    code_unite_mesure = models.CharField(db_column='Code_Unite_Mesure', primary_key=True, max_length=4)  # Field name made lowercase.
    symbole_unite = models.CharField(db_column='Symbole_Unite', max_length=10, blank=True, null=True)  # Field name made lowercase.
    libelle_unite = models.CharField(db_column='Libelle_Unite', max_length=50, blank=True, null=True)  # Field name made lowercase.
    est_bloquer = models.BooleanField(db_column='Est_Bloquer', blank=True, null=True)  # Field name made lowercase.
    user_id = models.CharField(db_column='User_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    date_modification = models.DateTimeField(db_column='Date_Modification', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tab_unite_de_mesure'


class TabProduction(models.Model):
    id_production = models.AutoField(db_column='ID_Production', primary_key=True)  # Field name made lowercase.
    code_type_production = models.ForeignKey('TabTypeProduction', models.DO_NOTHING, db_column='Code_Type_Production')  # Field name made lowercase.
    code_site = models.ForeignKey('TabActiviteTaches', models.DO_NOTHING, db_column='Code_site', to_field='NT')  # Field name made lowercase.
    code_filiale = models.CharField(db_column='Code_Filiale', max_length=5, blank=True, null=True)  # Field name made lowercase.
    nt = models.ForeignKey('TabActiviteTaches', models.DO_NOTHING, db_column='NT', to_field='NT', related_name='tabproduction_nt_set', blank=True, null=True)  # Field name made lowercase.
    code_groupeactivite = models.ForeignKey('TabActiviteTaches', models.DO_NOTHING, db_column='Code_GroupeActivite', to_field='NT', related_name='tabproduction_code_groupeactivite_set', blank=True, null=True)  # Field name made lowercase.
    code_activite = models.ForeignKey('TabActiviteTaches', models.DO_NOTHING, db_column='Code_Activite', to_field='NT', related_name='tabproduction_code_activite_set', blank=True, null=True)  # Field name made lowercase.
    code_tache = models.ForeignKey('TabActiviteTaches', models.DO_NOTHING, db_column='Code_Tache', to_field='NT', related_name='tabproduction_code_tache_set', blank=True, null=True)  # Field name made lowercase.
    recepteur = models.CharField(db_column='Recepteur', max_length=20, blank=True, null=True)  # Field name made lowercase.
    code_produit = models.ForeignKey('TabProduitManufacture', models.DO_NOTHING, db_column='Code_Produit', blank=True, null=True)  # Field name made lowercase.
    code_unite_mesure = models.ForeignKey(TabUniteDeMesure, models.DO_NOTHING, db_column='Code_Unite_Mesure', blank=True, null=True)  # Field name made lowercase.
    type_prestation = models.SmallIntegerField(db_column='Type_Prestation', blank=True, null=True)  # Field name made lowercase.
    mmaa = models.DateField(db_column='Mmaa')  # Field name made lowercase.
    quantite_1 = models.FloatField(db_column='Quantite_1', blank=True, null=True)  # Field name made lowercase.
    valeur_1 = models.DecimalField(db_column='Valeur_1', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    quantite_2 = models.FloatField(db_column='Quantite_2', blank=True, null=True)  # Field name made lowercase.
    valeur_2 = models.DecimalField(db_column='Valeur_2', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    quantite_3 = models.FloatField(db_column='Quantite_3', blank=True, null=True)  # Field name made lowercase.
    valeur_3 = models.DecimalField(db_column='Valeur_3', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    prevu_realiser = models.CharField(db_column='Prevu_Realiser', max_length=1)  # Field name made lowercase.
    est_cloturer = models.BooleanField(db_column='Est_Cloturer', blank=True, null=True)  # Field name made lowercase.
    user_id = models.CharField(db_column='User_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    date_modification = models.DateTimeField(db_column='Date_Modification', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tab_production'
