from datetime import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# Create your models here.
class Images(models.Model):
    key = models.BigAutoField(primary_key=True)
    src = models.ImageField(upload_to="Images/Login", null=False, blank=True, default='default.png')
    est_bloquer = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        self.est_bloquer = not self.est_bloquer
        super(Images, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Images'
        verbose_name_plural = 'Images'


class Clients(models.Model):
    code_client = models.CharField(db_column='Code_Client', primary_key=True, max_length=500)
    type_client = models.PositiveSmallIntegerField(db_column='Type_Client', blank=True, null=True)
    est_client_cosider = models.BooleanField(db_column='Est_Client_Cosider', blank=True, null=False)
    libelle_client = models.CharField(db_column='Libelle_Client', max_length=300, blank=True, null=True)
    nif = models.CharField(db_column='NIF', unique=True, max_length=50, blank=True, null=True)
    raison_social = models.CharField(db_column='Raison_Social', max_length=50, blank=True, null=True)
    num_registre_commerce = models.CharField(db_column='Num_Registre_Commerce', max_length=20, blank=True, null=True)
    est_bloquer = models.BooleanField(default=False, db_column='Est_Bloquer', null=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='User_ID', editable=False)
    date_modification = models.DateTimeField(db_column='Date_Modification', editable=False, auto_now=True)

    def __str__(self):
        return self.code_client + ' ' + self.libelle_client

    def delete(self, *args, **kwargs):
        self.est_bloquer = not self.est_bloquer
        self.date_modification = datetime.now()
        super(Clients, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Clients'
        verbose_name_plural = 'Clients'


class Sites(models.Model):
    code_site = models.CharField(db_column='Code_site', primary_key=True, max_length=10)
    code_filiale = models.CharField(db_column='Code_Filiale', max_length=5)
    code_region = models.CharField(db_column='Code_Region', max_length=1, blank=True, null=True)
    libelle_site = models.CharField(db_column='Libelle_Site', max_length=150, blank=True, null=True)
    code_agence = models.CharField(db_column='Code_Agence', max_length=15, blank=True, null=True)
    type_site = models.PositiveSmallIntegerField(db_column='Type_Site', blank=True, null=True)
    code_division = models.CharField(db_column='Code_Division', max_length=15, blank=True, null=True)
    code_commune_site = models.CharField(db_column='Code_Commune_Site', max_length=10, blank=True, null=True)
    jour_cloture_mouv_rh_paie = models.CharField(db_column='Jour_Cloture_Mouv_RH_Paie', max_length=2, blank=True,
                                                 null=True)
    date_ouverture_site = models.DateField(db_column='Date_Ouverture_Site', blank=True, null=True)
    date_cloture_site = models.DateField(db_column='Date_Cloture_Site', blank=True, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='User_ID', editable=False)
    est_bloquer = models.BooleanField(db_column='Est_Bloquer', null=False, default=False)
    date_modification = models.DateTimeField(db_column='Date_Modification', null=False, auto_now=True)

    def __str__(self):
        return self.code_site

    def save(self, *args, **kwargs):
        if (self.date_cloture_site >= self.date_ouverture_site):
            self.date_modification = datetime.now()
            super(Sites, self).save(*args, **kwargs)

        else:
            raise ValidationError("Date de cloture doit etre supérieur ou égale à la date d\'ouverture")

    def delete(self, *args, **kwargs):
        self.est_bloquer = not self.est_bloquer
        super(Sites, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Sites'
        verbose_name_plural = 'Sites'


class NT(models.Model):
    code_site = models.ForeignKey(Sites, models.DO_NOTHING, db_column='Code_site', null=False)
    nt = models.CharField(db_column='NT', max_length=20, null=False)
    code_client = models.ForeignKey(Clients, models.DO_NOTHING, db_column='Code_Client')
    # code_situation_nt = models.ForeignKey('TabSituationNt', models.DO_NOTHING, db_column='Code_Situation_NT', blank=True, null=True)
    libelle_nt = models.TextField(db_column='Libelle_NT', blank=True, null=True)
    date_ouverture_nt = models.DateField(db_column='Date_Ouverture_NT', blank=True, null=True)
    date_cloture_nt = models.DateField(db_column='Date_Cloture_NT', blank=True, null=True)
    est_bloquer = models.BooleanField(db_column='Est_Bloquer', null=False, default=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='User_ID', editable=False)
    date_modification = models.DateTimeField(db_column='Date_Modification', null=False, auto_now=True)

    def __str__(self):
        return str(self.code_site.code_site) + " " + str(self.nt)

    def save(self, *args, **kwargs):
        if (self.date_cloture_nt >= self.date_ouverture_nt):
            self.date_modification = datetime.now()
            super(NT, self).save(*args, **kwargs)
        else:
            raise ValidationError("Date de cloture doit etre supérieur ou égale à la date d\'ouverture")

    def delete(self, *args, **kwargs):
        self.date_modification = datetime.now()
        self.est_bloquer = not self.est_bloquer
        super(NT, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'NT'
        verbose_name_plural = 'NT'
        unique_together = (('code_site', 'nt'),)


class Marche(models.Model):
    nt = models.ForeignKey(NT, models.DO_NOTHING, db_column='numero_marche', null=False)
    avenant = models.PositiveBigIntegerField(default=0, db_column='avenant', null=False)
    libelle = models.CharField(null=False, blank=True, max_length=500)
    ods_depart = models.DateField(null=False, blank=True)
    delais = models.PositiveIntegerField(default=0, null=False)
    ht = models.DecimalField(
        max_digits=10, decimal_places=2, editable=False,
        validators=[MinValueValidator(0)], default=0
    )
    ttc = models.DecimalField(
        max_digits=10, decimal_places=2, editable=False,
        validators=[MinValueValidator(0)], default=0
    )
    revisable = models.BooleanField(default=True, null=False)
    rabais = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)],
                                         null=False)
    tva = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)], null=False)
    code_contrat = models.CharField(null=False, blank=True, max_length=20)
    date_signature = models.DateTimeField(db_column='Date_Signature', null=False, auto_now=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='User_ID', editable=False)
    date_modification = models.DateTimeField(db_column='Date_Modification', null=False, auto_now=True)

    def __str__(self):
        return self.nt.code_site.code_site + self.nt.nt + str(self.avenant)

    def save(self, *args, **kwargs):
        self.ttc = self.ht + (self.ht * self.tva)
        self.date_modification = datetime.now()
        super(Marche, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.est_bloquer = not self.est_bloquer
        super(NT, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Marchés'
        verbose_name_plural = 'Marchés'


class DQE(models.Model):
    marche = models.ForeignKey(Marche, models.DO_NOTHING,null=False)
    designation = models.CharField(max_length=600, null=False)
    prix_u = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0)], default=0
    )
    unite = models.CharField(max_length=5, null=False)
    quantite = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    prix_q = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default=0,
                                 editable=False)

    def save(self, *args, **kwargs):
        self.prix_q = self.quantite * self.prix_u
        dqe=DQE.objects.filter(marche=self.marche)
        marche=Marche.objects.get(id=self.marche.id)
        ht=0
        for d in dqe:
            ht=ht+d.prix_q
        marche.ht=ht
        marche.save()


        super(DQE, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'DQE'
        verbose_name_plural = 'DQE'




