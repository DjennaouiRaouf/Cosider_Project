# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class TabGroupeactiviteActivite(models.Model):
    code_groupeactivite = models.OneToOneField('TabGroupeactivite', models.DO_NOTHING, db_column='Code_GroupeActivite', primary_key=True)  # Field name made lowercase. The composite primary key (Code_GroupeActivite, Code_Activite) found, that is not supported. The first column is selected.
    code_activite = models.ForeignKey('TabActivite', models.DO_NOTHING, db_column='Code_Activite')  # Field name made lowercase.
    est_bloquer = models.BooleanField(db_column='Est_Bloquer', blank=True, null=True)  # Field name made lowercase.
    user_id = models.CharField(db_column='User_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    date_modification = models.DateTimeField(db_column='Date_Modification', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Tab_GroupeActivite_Activite'
        unique_together = (('code_groupeactivite', 'code_activite'),)
