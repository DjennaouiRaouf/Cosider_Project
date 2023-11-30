from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from safedelete import SOFT_DELETE_CASCADE, DELETED_VISIBLE_BY_PK, SOFT_DELETE
from safedelete.managers import SafeDeleteManager
from safedelete.models import SafeDeleteModel
from simple_history.models import HistoricalRecords


class DeletedModelManager(SafeDeleteManager):
    _safedelete_visibility = DELETED_VISIBLE_BY_PK

# Create your models here.
class Images(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    key = models.BigAutoField(primary_key=True)
    src = models.ImageField(upload_to="Images/Login", null=False, blank=True, default='default.png')
    history = HistoricalRecords()
    objects = DeletedModelManager()


    class Meta:
        verbose_name = 'Images'
        verbose_name_plural = 'Images'




class Clients(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    code_client = models.CharField(db_column='Code_Client', primary_key=True, max_length=500, verbose_name='Code du Client')
    type_client = models.PositiveSmallIntegerField(db_column='Type_Client', blank=True, null=True ,verbose_name='Type de Client')
    est_client_cosider = models.BooleanField(db_column='Est_Client_Cosider', blank=True, null=False
                                             ,verbose_name='Est Client Cosider')
    libelle_client = models.CharField(db_column='Libelle_Client', max_length=300, blank=True, null=True,
                                      verbose_name='Libelle')
    nif = models.CharField(db_column='NIF', unique=True, max_length=50, blank=True, null=True,verbose_name='NIF')
    raison_social = models.CharField(db_column='Raison_Social', max_length=50, blank=True, null=True,verbose_name='Raison Social')
    num_registre_commerce = models.CharField(db_column='Num_Registre_Commerce', max_length=20, blank=True, null=True,
                                             verbose_name='Numero du registre de commerce')
    history = HistoricalRecords()
    objects = DeletedModelManager()
    def __str__(self):
        return "Client: " + self.code_client



    class Meta:
        verbose_name = 'Clients'
        verbose_name_plural = 'Clients'


class Sites(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
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
    date_ouverture_site = models.DateField(db_column='Date_Ouverture_Site', blank=True, null=False)
    date_cloture_site = models.DateField(db_column='Date_Cloture_Site', blank=True, null=True)

    history = HistoricalRecords()
    objects = DeletedModelManager()

    def __str__(self):
        return "Site: " + self.code_site

    def save(self, *args, **kwargs):
        if (self.date_cloture_site >= self.date_ouverture_site):
            super(Sites, self).save(*args, **kwargs)
        else:
            raise ValidationError("Date de cloture doit etre supérieur ou égale à la date d\'ouverture")




    class Meta:
        verbose_name = 'Sites'
        verbose_name_plural = 'Sites'


class NT(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    code_site = models.ForeignKey(Sites, on_delete=models.CASCADE, db_column='Code_site', null=False)
    nt = models.CharField(db_column='NT', max_length=20, null=False)
    code_client = models.ForeignKey(Clients, on_delete=models.CASCADE, db_column='Code_Client',null=False)
    # code_situation_nt = models.ForeignKey('TabSituationNt', on_delete=models.CASCADE, db_column='Code_Situation_NT', blank=True, null=True)
    libelle_nt = models.CharField(max_length=900,db_column='Libelle_NT', blank=True, null=True)
    date_ouverture_nt = models.DateField(db_column='Date_Ouverture_NT', blank=True, null=True)
    date_cloture_nt = models.DateField(db_column='Date_Cloture_NT', blank=True, null=True)
    history = HistoricalRecords()
    objects = DeletedModelManager()

    def __str__(self):
        return "Site: " + str(self.code_site.code_site) + " Nt: " + str(self.nt)

    def save(self, *args, **kwargs):
        if (self.date_cloture_nt >= self.date_ouverture_nt):
            super(NT, self).save(*args, **kwargs)
        else:
            raise ValidationError("Date de cloture doit etre supérieur ou égale à la date d\'ouverture")



    class Meta:
        verbose_name = 'Numero du travail'
        verbose_name_plural = 'Numero du travail'
        unique_together = (('code_site', 'nt'),)


class Marche(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    nt = models.ForeignKey(NT, on_delete=models.CASCADE, db_column='numero_marche', null=False)
    num_avenant = models.PositiveIntegerField(default=0, null=False, editable=False)
    libelle = models.CharField(null=False, blank=True, max_length=500)
    ods_depart = models.DateField(null=False, blank=True)
    delais = models.PositiveIntegerField(default=0, null=False)
    revisable = models.BooleanField(default=True, null=False)
    rabais = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)],
                                         null=False)
    tva = models.DecimalField(default=0, max_digits=38, decimal_places=2,
                              validators=[MinValueValidator(0), MaxValueValidator(100)], null=False)
    retenue_de_garantie = models.DecimalField(default=0, max_digits=38, decimal_places=2,
                              validators=[MinValueValidator(0), MaxValueValidator(100)], null=False)
    code_contrat = models.CharField(null=False, blank=True, max_length=20)
    date_signature = models.DateField(null=False)
    history = HistoricalRecords()
    objects = DeletedModelManager()

    def __str__(self):
        return "Site: " + self.nt.code_site.code_site + " Nt: " + self.nt.nt + " Av: " + str(self.num_avenant)

    @property
    def ht(self):
        dqe = DQE.objects.filter(marche=self.id)
        sum = 0
        for i in dqe:
            sum = sum + i.prix_q
        return sum

    @property
    def ttc(self):
        ttc=round(self.ht + (self.ht * self.tva / 100), 2)
        return ttc

    def save(self, *args, **kwargs):
        count = Marche.objects.filter(nt=self.nt).count()
        self.num_avenant=count
        super(Marche, self).save(*args, **kwargs)



    class Meta:
        verbose_name = 'Marchés'
        verbose_name_plural = 'Marchés'
        unique_together=(('nt','num_avenant'),)





class DQE(SafeDeleteModel): # le prix final
    _safedelete_policy = SOFT_DELETE_CASCADE
    marche = models.ForeignKey(Marche,on_delete=models.CASCADE,  null=False)
    designation = models.CharField(max_length=600, null=False)
    unite = models.CharField(max_length=5, null=False)
    prix_u = models.DecimalField(
        max_digits=38, decimal_places=2,
        validators=[MinValueValidator(0)], default=0
    )

    quantite = models.DecimalField(max_digits=38, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    history = HistoricalRecords()
    objects = DeletedModelManager()


    def __str__(self):
        return (str(self.marche) + " " + self.designation)

    @property
    def prix_q(self):
        return round(self.quantite * self.prix_u,2)


    def save(self, *args, **kwargs):
            super(DQE, self).save(*args, **kwargs)




    class Meta:
        verbose_name = 'DQE'
        verbose_name_plural = 'DQE'
        unique_together = (("marche", "designation"))




class Ordre_De_Service(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    marche = models.ForeignKey(Marche, on_delete=models.CASCADE, null=True, related_name="ods_marche")
    date_interruption = models.DateField(null=False, blank=True)
    date_reprise = models.DateField(null=False, blank=True)
    motif = models.TextField(null=False, blank=True)
    history = HistoricalRecords()
    objects = DeletedModelManager()

    def save(self, *args, **kwargs):
       if (self.date_reprise > self.date_interruption):
            super(Ordre_De_Service, self).save(*args, **kwargs)


    class Meta:
        verbose_name = 'Ordre de service'
        verbose_name_plural = 'Ordre de service'


class TypeCaution(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    libelle = models.CharField(max_length=500, null=False)
    taux = models.DecimalField(default=0, max_digits=38, decimal_places=2,
                               validators=[MinValueValidator(0), MaxValueValidator(100)], null=False)
    history = HistoricalRecords()
    objects = DeletedModelManager()

    def __str__(self):
        return self.libelle

    def save(self, *args, **kwargs):
        super(TypeCaution, self).save(*args, **kwargs)



    class Meta:
        verbose_name = 'Type_Caution'
        verbose_name_plural = 'Type_Caution'


class Banque(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE
    nom = models.CharField(max_length=300, null=False)
    adresse = models.CharField(max_length=300, null=False)
    ville = models.CharField(max_length=300, null=False)
    wilaya = models.CharField(max_length=300, null=False)
    history = HistoricalRecords()
    objects = DeletedModelManager()

    def save(self, *args, **kwargs):
        super(Banque, self).save(*args, **kwargs)




    def __str__(self):
        return self.nom + " " + self.ville + '(' + self.wilaya + ')'

    class Meta:
        verbose_name = 'Banque'
        verbose_name_plural = 'Banque'


class TypeAvance(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    libelle = models.CharField(max_length=500, null=False, unique=True)
    history = HistoricalRecords()
    objects = DeletedModelManager()

    def __str__(self):
        return self.libelle

    def save(self, *args, **kwargs):
        super(TypeAvance, self).save(*args, **kwargs)




    class Meta:
        verbose_name = 'Type Avance'
        verbose_name_plural = 'Type Avance'


class Avance(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    marche = models.ForeignKey(Marche, on_delete=models.CASCADE, null=False, related_name="Avance_Marche")
    type = models.ForeignKey(TypeAvance, on_delete=models.CASCADE, null=False)
    montant = models.DecimalField(max_digits=38, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    Client = models.ForeignKey(Marche, on_delete=models.CASCADE, null=False, related_name="Avance_Client")
    history = HistoricalRecords()
    objects = DeletedModelManager()


    def save(self, *args, **kwargs):
        super(Avance, self).save(*args, **kwargs)




class Cautions(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    marche = models.ForeignKey(Marche, on_delete=models.CASCADE, null=False, related_name="Caution_Marche")
    type = models.ForeignKey(TypeCaution, on_delete=models.CASCADE, null=False)
    avance = models.ForeignKey(Avance, on_delete=models.CASCADE, null=True, blank=True)
    date_soumission = models.DateField(blank=True, null=False)
    banque = models.ForeignKey(Banque, on_delete=models.CASCADE, null=False)
    montant = models.DecimalField(
        max_digits=38, decimal_places=2,
        validators=[MinValueValidator(0)], default=0,
        editable=False
    )
    est_recupere = models.BooleanField(default=True, null=False, editable=False)
    history = HistoricalRecords()
    objects = DeletedModelManager()

    def recuperation(self):
        self.est_recupere = True  # la caution est récupérée

    def soumission(self):
        if (self.avance and self.avance.type.libelle == self.type.libelle):
            taux_c = TypeCaution.objects.get(libelle=self.avance.type.libelle).taux
            self.montant = self.avance.montant * taux_c
        if (not self.avance):
            self.montant = (self.marche.ttc * self.type.taux) / 100

        self.est_recupere = False  # la caution est déposée

    def save(self, *args, **kwargs):
        self.soumission()

        super(Cautions, self).save(*args, **kwargs)



    class Meta:
        verbose_name = 'Caution'
        verbose_name_plural = 'Caution'


class Attachements(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    dqe = models.ForeignKey(DQE, on_delete=models.CASCADE)
    qte_realise = models.DecimalField(max_digits=38, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    qte_restante = models.DecimalField(max_digits=38, decimal_places=2, validators=[MinValueValidator(0)], default=0, editable=False)
    history = HistoricalRecords()
    objects = DeletedModelManager()

    @property
    def taux(self):
        taux = round(self.qte_realise * 100 / self.dqe.quantite, 2)
        return taux
    @property
    def montant_estime(self):
        montant_e= round(self.dqe.prix_u * self.qte_realise,2)
        return montant_e

    @property
    def montant_rg(self):
        rg = self.dqe.marche.retenue_de_garantie
        montant_rg = round(rg * self.montant_estime / 100, 2)
        return montant_rg

    @property
    def montant_rb(self):
        rb = self.dqe.marche.rabais
        montant_rb = round(rb * self.montant_estime/ 100, 2)
        return montant_rb

    @property
    def montant_final(self):
        montant_final = round(self.montant_estime- self.montant_rg - self.montant_rb,2)
        return montant_final

    def __str__(self):
        return  self.dqe.designation

    def save(self, *args, **kwargs):
        sum=Attachements.objects.filter(dqe__designation=self.dqe.designation).aggregate(models.Sum('qte_realise'))[
            "qte_realise__sum"]
        if sum == None:
            sum = 0
        sum = sum + self.qte_realise
        self.qte_restante = round(self.dqe.quantite- sum, 2)
        if (self.qte_restante > 0):
            super(Attachements, self).save(*args, **kwargs)
        else:
            raise ValidationError('Qte realisée ne doit pas dépasser le Qte prévue dans le DQE')




    class Meta:
        verbose_name = 'Attachements'
        verbose_name_plural = 'Attachements'




class Factures(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    numero_facture=models.CharField(max_length=500,primary_key=True)
    date_facture=models.DateField(null=False,auto_now=True)
    payer = models.BooleanField(default=False, null=False)
    client=models.ForeignKey(Clients,on_delete=models.CASCADE,null=False)
    history = HistoricalRecords()
    objects = DeletedModelManager()
    @property
    def montant_global(self):  # paiement complet ou incomplet
        df=DetailFacture.objects.filter(facture=self)
        mg=0
        for d in df:
            mg+=d.detail.montant_final
        return round(mg,2)

    def delete(self, *args, **kwargs):
       super(Factures, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Factures'
        verbose_name_plural = 'Factures'

class DetailFacture(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    facture=models.ForeignKey(Factures,on_delete=models.CASCADE,null=False,blank=True)
    detail=models.ForeignKey(Attachements,on_delete=models.CASCADE)
    history = HistoricalRecords()
    objects = DeletedModelManager()


    class Meta:
        verbose_name = 'Datails Facture'
        verbose_name_plural = 'Details Facture'
        unique_together=(("facture","detail"),)

class Encaissement(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    facture=models.ForeignKey(Factures,on_delete=models.CASCADE,null=False,blank=True)
    date_encaissement=models.DateField(null=False)
    mode_paiement=models.CharField(max_length=100,null=False)
    montant_encaisse=models.DecimalField(max_digits=38, decimal_places=2, blank=True,
                                     validators=[MinValueValidator(0)], default=0)
    montant_creance = models.DecimalField(max_digits=38, decimal_places=2, blank=True,
                                           validators=[MinValueValidator(0)], default=0,editable=False)
    banque=models.ForeignKey(Banque,on_delete=models.CASCADE,null=False)
    numero_piece = models.CharField(max_length=300,null=False)
    objects = DeletedModelManager()

    def save(self, *args, **kwargs):
        sum = Encaissement.objects.filter(facture=self.facture).aggregate(models.Sum('montant_encaisse'))[
            "montant_encaisse__sum"]
        if(sum==None):
            sum=0
        sum=sum+self.montant_encaisse
        self.montant_creance = round(self.facture.montant_global - sum,2)
        if(self.montant_creance >= 0):
            super(Encaissement, self).save(*args, **kwargs)
        else:
            raise ValidationError('Le paiement de la facture est terminer')



    class Meta:
        verbose_name = 'Encaissement'
        verbose_name_plural = 'Encaissement'
        unique_together=(("facture","date_encaissement"),)





