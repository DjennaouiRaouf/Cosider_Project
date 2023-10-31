from django.contrib.auth.models import User
from django.db import models
from colorfield.fields import ColorField

# Create your models here.
class Images(models.Model):
    key = models.BigAutoField(primary_key=True)
    src=models.ImageField(upload_to="Images/Login",null=False,blank=True,default='default.png')
    visible=models.BooleanField(default=True)
    def delete(self, *args, **kwargs):
        self.visible=False
        super(Images, self).save(*args, **kwargs)
    class Meta:
        verbose_name = 'Images'
        verbose_name_plural = 'Images'


class Clients(models.Model):
    code_client = models.CharField(db_column='Code_Client', primary_key=True, max_length=500)  # Field name made lowercase.
    type_client = models.SmallIntegerField(db_column='Type_Client', blank=True, null=True)  # Field name made lowercase.
    est_client_cosider = models.BooleanField(db_column='Est_Client_Cosider', blank=True, null=False)  # Field name made lowercase.
    libelle_client = models.CharField(db_column='Libelle_Client', max_length=300, blank=True, null=True)  # Field name made lowercase.
    nif = models.CharField(db_column='NIF', unique=True, max_length=50, blank=True, null=True)  # Field name made lowercase.
    raison_social = models.CharField(db_column='Raison_Social', max_length=50, blank=True, null=True)  # Field name made lowercase.
    num_registre_commerce = models.CharField(db_column='Num_Registre_Commerce', max_length=20, blank=True, null=True)  # Field name made lowercase.
    est_bloquer = models.BooleanField(default=False,db_column='Est_Bloquer', blank=True, null=True)  # Field name made lowercase.
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,db_column='User_ID',  blank=True, null=False)  # Field name made lowercase.
    date_modification = models.DateTimeField(db_column='Date_Modification', blank=True, null=True, auto_now=True)  # Field name made lowercase.

    class Meta:
        verbose_name = 'Clients'
        verbose_name_plural = 'Clients'





class Sites(models.Model):

    code_site = models.CharField(db_column='Code_site', primary_key=True, max_length=10)  # Field name made lowercase.
    code_filiale = models.CharField(db_column='Code_Filiale', max_length=5)  # Field name made lowercase.
    code_region = models.CharField(db_column='Code_Region', max_length=1, blank=True, null=True)  # Field name made lowercase.
    libelle_site = models.CharField(db_column='Libelle_Site', max_length=150, blank=True, null=True)  # Field name made lowercase.
    code_agence = models.CharField(db_column='Code_Agence', max_length=15, blank=True, null=True)  # Field name made lowercase.
    type_site = models.SmallIntegerField(db_column='Type_Site', blank=True, null=True)  # Field name made lowercase.
    code_division = models.CharField(db_column='Code_Division', max_length=15, blank=True, null=True)  # Field name made lowercase.
    code_commune_site = models.CharField(db_column='Code_Commune_Site', max_length=10, blank=True, null=True)  # Field name made lowercase.
    jour_cloture_mouv_rh_paie = models.CharField(db_column='Jour_Cloture_Mouv_RH_Paie', max_length=2, blank=True, null=True)  # Field name made lowercase.
    date_ouverture_site = models.DateField(db_column='Date_Ouverture_Site', blank=True, null=True)  # Field name made lowercase.
    date_cloture_site = models.DateField(db_column='Date_Cloture_Site', blank=True, null=True)  # Field name made lowercase.
    est_bloquer = models.BooleanField(db_column='Est_Bloquer', blank=True, null=True)  # Field name made lowercase.
    user_id = models.CharField(db_column='User_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    date_modification = models.DateTimeField(db_column='Date_Modification', blank=True, null=True)  # Field name made lowercase.
    class Meta:
        verbose_name = 'Sites'
        verbose_name_plural = 'Sites'

