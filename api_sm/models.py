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

    adresse = models.CharField(db_column='adresse', max_length=500, blank=True, null=True,
                                      verbose_name='Adresse')

    nif = models.CharField(db_column='NIF', unique=True, max_length=50, blank=True, null=True,verbose_name='NIF')
    raison_social = models.CharField(db_column='Raison_Social', max_length=50, blank=True, null=True,verbose_name='Raison Social')
    num_registre_commerce = models.CharField(db_column='Num_Registre_Commerce', max_length=20, blank=True, null=True,
                                             verbose_name='Numero du registre de commerce')
    
    objects = DeletedModelManager()
    def __str__(self):
        return  self.code_client



    class Meta:
        verbose_name = 'Clients'
        verbose_name_plural = 'Clients'


class Sites(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    code_site = models.CharField(db_column='Code_site', primary_key=True, max_length=500 ,
                                 verbose_name='Code du Site')
    responsable_site = models.CharField(db_column='Responsable', max_length=500, blank=True, null=True,
                                 verbose_name='Responsable du Site')
    libelle_site = models.CharField(db_column='Libelle_Site', max_length=500, blank=True, null=True,
                                 verbose_name='Libelle du Site')
    type_site = models.PositiveSmallIntegerField(db_column='Type_Site', blank=True, null=True,
                                 verbose_name='Type du Site')

    code_filiale = models.CharField(db_column='Code_Filiale', max_length=50,blank=True, null=True,
                                 verbose_name='Code Filiale')
    code_division = models.CharField(db_column='Code_Division', max_length=50, blank=True, null=True,
                                 verbose_name='Code division')

    code_region = models.CharField(db_column='Code_Region', max_length=20, blank=True, null=True,
                                 verbose_name='Code région')
    code_commune_site = models.CharField(db_column='Code_Commune_Site', max_length=50, blank=True, null=True,
                                 verbose_name='Code commune')

    date_ouverture_site = models.DateField(db_column='Date_Ouverture_Site', blank=True, null=True,
                                 verbose_name='Ouverture')
    date_cloture_site = models.DateField(db_column='Date_Cloture_Site', blank=True, null=True,
                                 verbose_name='Cloture')

    
    objects = DeletedModelManager()

    def __str__(self):
        return self.code_site

    def save(self, *args, **kwargs):
        if self.date_cloture_site and self.date_ouverture_site:
            if (self.date_cloture_site >= self.date_ouverture_site):
                super(Sites, self).save(*args, **kwargs)
            else:
                raise ValidationError("Date de cloture doit etre supérieur ou égale à la date d\'ouverture")
        if self.date_ouverture_site == None and self.date_cloture_site == None:
            super(Sites, self).save(*args, **kwargs)
        if( self.date_ouverture_site and self.date_cloture_site == None ):
            super(Sites, self).save(*args, **kwargs)



    class Meta:
        verbose_name = 'Sites'
        verbose_name_plural = 'Sites'


class SituationNt(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    libelle=models.CharField(max_length=100,null=False,unique=True)
    
    objects = DeletedModelManager()
    class Meta:
        verbose_name = 'Situation du Travail'
        verbose_name_plural = 'Situation du Travail'

    def __str__(self):
        return  self.libelle
    def save(self, *args, **kwargs):
            self.libelle=self.libelle.lower()
            super(SituationNt, self).save(*args, **kwargs)




class NT(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    id=models.CharField(db_column='id',max_length=500,primary_key=True,verbose_name="id",editable=False)
    nt = models.CharField(db_column='NT', max_length=20, verbose_name='Numero du travail')
    code_site = models.ForeignKey(Sites, on_delete=models.CASCADE, db_column='Code_site', null=False,to_field='code_site'
                                  , verbose_name='Code du Site')
    code_client = models.ForeignKey(Clients, on_delete=models.CASCADE, db_column='Code_Client',null=True
                                    , verbose_name='Code du client')
    code_situation_nt = models.ForeignKey(SituationNt, on_delete=models.CASCADE, blank=True, null=True
                                          , verbose_name='Situation')
    libelle_nt = models.CharField(max_length=900,db_column='Libelle_NT', blank=True, null=True
                                  , verbose_name='Libelle')
    date_ouverture_nt = models.DateField(db_column='Date_Ouverture_NT', blank=True, null=True
                                         , verbose_name='Ouverture')
    date_cloture_nt = models.DateField(db_column='Date_Cloture_NT', blank=True, null=True
                                       , verbose_name='Cloture')
    
    objects = DeletedModelManager()

    def __str__(self):
        return str(self.nt)

    class Meta:
        verbose_name = 'Numero du travail'
        verbose_name_plural = 'Numero du travail'
        unique_together = (('code_site', 'nt'),)


class Marche(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    id=models.CharField(max_length=500,primary_key=True,editable=False,verbose_name='id')
    nt = models.ForeignKey(NT, on_delete=models.CASCADE, db_column='nt', null=False
                           , verbose_name='Numero Travail',to_field="id")

    num_avenant = models.PositiveIntegerField(default=0, null=False, editable=False
                                              , verbose_name='Avenant Numero')
    libelle = models.CharField(null=False, blank=True, max_length=500
                               , verbose_name='Libelle')
    ods_depart = models.DateField(null=False, blank=True
                                  , verbose_name='ODS de départ')
    delais = models.PositiveIntegerField(default=0, null=False
                                         , verbose_name='Delai des traveaux')
    revisable = models.BooleanField(default=True, null=False
                                    , verbose_name='Est-il révisable ?')
    delai_paiement_f=models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)],
                                         null=True
                                                 , verbose_name='Delai de paiement')
    rabais = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)],
                                         null=False , verbose_name='Taux de rabais')
    ht=models.DecimalField(default=0, max_digits=38, decimal_places=2,  verbose_name='Prix Hors taxe',
                              validators=[MinValueValidator(0), MaxValueValidator(100)], null=False,editable=False)
    ttc = models.DecimalField(default=0, max_digits=38, decimal_places=2, verbose_name='Prix avec taxe',
                                  validators=[MinValueValidator(0), MaxValueValidator(100)], null=False, editable=False)

    tva = models.DecimalField(default=0, max_digits=38, decimal_places=2, verbose_name='TVA',
                              validators=[MinValueValidator(0), MaxValueValidator(100)], null=False)
    rg = models.DecimalField(default=0, max_digits=38, decimal_places=2,
                              validators=[MinValueValidator(0), MaxValueValidator(100)], null=False
                                              , verbose_name='Retenue de garantie')
    code_contrat = models.CharField(null=False, blank=True, max_length=20, verbose_name='Code du contrat')
    date_signature = models.DateField(null=False, verbose_name='Date de signature')
    
    objects = DeletedModelManager()

    def __str__(self):
        return self.id

    def save(self, *args, **kwargs):
        super(Marche, self).save(*args, **kwargs)


class Meta:
        verbose_name = 'Marchés'
        verbose_name_plural = 'Marchés'
        unique_together=(('nt','num_avenant'),)





class DQE(SafeDeleteModel): # le prix final
    _safedelete_policy = SOFT_DELETE_CASCADE
    marche = models.ForeignKey(Marche,on_delete=models.CASCADE,  null=False,related_name="marche_dqe",
                               to_field="id")
    designation = models.CharField(max_length=600, null=False,verbose_name='Designation')
    unite = models.CharField(max_length=5, null=False,verbose_name='Unité de mesure')
    prix_u = models.DecimalField(
        max_digits=38, decimal_places=2,
        validators=[MinValueValidator(0)], default=0
        ,verbose_name='Prix unitaire'
    )
    prix_q = models.DecimalField(
        max_digits=38, decimal_places=2,
        validators=[MinValueValidator(0)], default=0,editable=False
        ,verbose_name='Montant'
    )

    quantite = models.DecimalField(max_digits=38, decimal_places=2, validators=[MinValueValidator(0)], default=0,verbose_name='Quantité')
    
    objects = DeletedModelManager()


    def __str__(self):
        return (str(self.marche) + " " + self.designation)


    def save(self, *args, **kwargs):
            super(DQE,self).save(*args, **kwargs)








    class Meta:
        verbose_name = 'DQE'
        verbose_name_plural = 'DQE'
        unique_together = (("marche", "designation",))




class Ordre_De_Service(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    marche = models.ForeignKey(Marche, on_delete=models.CASCADE, null=True, related_name="ods_marche")
    date_interruption = models.DateField(null=False, blank=True)
    date_reprise = models.DateField(null=False, blank=True)
    motif = models.TextField(null=False, blank=True)
    
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
    taux_reduction_facture=models.DecimalField(default=0, max_digits=38, decimal_places=2,
                               validators=[MinValueValidator(0), MaxValueValidator(100)], null=False)
    
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
    dqe = models.ForeignKey(DQE, on_delete=models.CASCADE)# item + quantité marche + prix unitaire
    qte_precedente = models.DecimalField(max_digits=38, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    qte_mois = models.DecimalField(max_digits=38, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    qte_cumule= models.DecimalField(max_digits=38, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    montant_precedent=models.DecimalField(max_digits=38, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    montant_mois= models.DecimalField(max_digits=38, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    montant_cumule = models.DecimalField(max_digits=38, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    date=models.DateField(null=False)

    objects = DeletedModelManager()


    def __str__(self):
        return  self.dqe.designation


    class Meta:
        verbose_name = 'Attachements'
        verbose_name_plural = 'Attachements'


class FactureRG(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

class Factures(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    numero_facture=models.PositiveBigIntegerField(primary_key=True)
    marche=models.ForeignKey(Marche,on_delete=models.CASCADE,null=True)
    du = models.DateField()
    au = models.DateField()
    paye = models.BooleanField(default=False, null=False,editable=False)

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





