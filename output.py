# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class TabFiliale(models.Model):
    code_filiale = models.CharField(db_column='Code_Filiale', primary_key=True, max_length=5)  # Field name made lowercase.
    code_entreprise = models.ForeignKey('TabEntreprise', models.DO_NOTHING, db_column='Code_Entreprise')  # Field name made lowercase.
    libelle_filiale = models.CharField(db_column='Libelle_Filiale', max_length=50, blank=True, null=True)  # Field name made lowercase.
    est_bloquer = models.BooleanField(db_column='Est_Bloquer', blank=True, null=True)  # Field name made lowercase.
    user_id = models.CharField(db_column='User_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    date_modification = models.DateTimeField(db_column='Date_Modification', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Tab_filiale'
