from django.db import models

# Create your models here.

class TabActivite(models.Model):
    code_activite = models.CharField(db_column='Code_Activite', primary_key=True, max_length=4)  # Field name made lowercase.
    libelle_activite = models.CharField(db_column='Libelle_Activite', max_length=50, blank=True, null=True)  # Field name made lowercase.
    je_l_utilise = models.BooleanField(db_column='Je_L_Utilise', blank=True, null=True)  # Field name made lowercase.
    est_bloquer = models.BooleanField(db_column='Est_Bloquer', blank=True, null=True)  # Field name made lowercase.
    user_id = models.CharField(db_column='User_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    date_modification = models.DateTimeField(db_column='Date_Modification', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Tab_Activite'
        app_label = 'api_sch'



class TabGroupeactivite(models.Model):
    code_groupeactivite = models.CharField(db_column='Code_GroupeActivite', primary_key=True, max_length=4)  # Field name made lowercase.
    libelle_groupeactivite = models.CharField(db_column='Libelle_GroupeActivite', max_length=50, blank=True, null=True)  # Field name made lowercase.
    je_l_utilise = models.BooleanField(db_column='Je_L_Utilise', blank=True, null=True)  # Field name made lowercase.
    est_bloquer = models.BooleanField(db_column='Est_Bloquer', blank=True, null=True)  # Field name made lowercase.
    user_id = models.CharField(db_column='User_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    date_modification = models.DateTimeField(db_column='Date_Modification', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Tab_GroupeActivite'


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

