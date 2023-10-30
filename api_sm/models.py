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
    est_client_cosider = models.BooleanField(default=False,db_column='Est_Client_Cosider', blank=True, null=True)  # Field name made lowercase.
    libelle_client = models.CharField(db_column='Libelle_Client', max_length=300, blank=True, null=True)  # Field name made lowercase.
    nif = models.CharField(db_column='NIF', unique=True, max_length=50, blank=True, null=True)  # Field name made lowercase.
    raison_social = models.CharField(db_column='Raison_Social', max_length=50, blank=True, null=True)  # Field name made lowercase.
    num_registre_commerce = models.CharField(db_column='Num_Registre_Commerce', max_length=20, blank=True, null=True)  # Field name made lowercase.
    est_bloquer = models.BooleanField(default=False,db_column='Est_Bloquer', blank=True, null=True)  # Field name made lowercase.
    user_id = models.CharField(db_column='User_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    date_modification = models.DateTimeField(db_column='Date_Modification', blank=True, null=True, auto_now=True)  # Field name made lowercase.

    class Meta:
        verbose_name = 'Clients'
        verbose_name_plural = 'Clients'


