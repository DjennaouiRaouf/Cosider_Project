from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from safedelete import SOFT_DELETE_CASCADE, DELETED_VISIBLE_BY_PK, SOFT_DELETE, HARD_DELETE
from safedelete.managers import SafeDeleteManager
from safedelete.models import SafeDeleteModel
from simple_history.models import HistoricalRecords

from api_sch.models import TabAgence


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
        app_label = 'api_sm'
        


class OptionImpression(SafeDeleteModel):
    Types = [
        ('H', 'Header'),
        ('F', 'Footer'),
    ]
    _safedelete_policy = SOFT_DELETE_CASCADE
    key = models.BigAutoField(primary_key=True)
    src = models.ImageField(upload_to="Images/Impression", null=False, blank=True)
    type=models.CharField( max_length=20,
        choices=Types, unique=True,null=False)
    objects = DeletedModelManager()
    class Meta:
        verbose_name = 'Option d\'Impression'
        verbose_name_plural = 'Option d\'Impression'
        app_label = 'api_sm'
        


class TabUniteDeMesure(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    libelle = models.CharField(db_column='Symbole_Unite', max_length=10, blank=True, null=True)
    description = models.CharField(db_column='Libelle_Unite', max_length=50, blank=True, null=True)
    objects = DeletedModelManager()

    def __str__(self):
        return self.libelle
    class Meta:
        verbose_name = 'Unite de Mesure'
        verbose_name_plural = 'Unite de Mesure'
        db_table = 'Tab_Unite_de_Mesure'
        app_label = 'api_sm'
        







class Clients(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    id = models.CharField(db_column='Code_Client', primary_key=True, max_length=500, verbose_name='Code du Client')
    type_client = models.PositiveSmallIntegerField(db_column='Type_Client', blank=True, null=True ,verbose_name='Type de Client')
    est_client_cosider = models.BooleanField(db_column='Est_Client_Cosider', blank=True, null=False
                                             ,verbose_name='Est Client Cosider')
    libelle = models.CharField(db_column='Libelle_Client', max_length=300, blank=True, null=True,
                                      verbose_name='Libelle')

    adresse = models.CharField(db_column='adresse', max_length=500, blank=True, null=True,
                                      verbose_name='Adresse')


    nif = models.CharField(db_column='NIF', unique=True, max_length=50, blank=True, null=True,verbose_name='NIF')
    raison_social = models.CharField(db_column='Raison_Social', max_length=50, blank=True, null=True,verbose_name='Raison Social')
    num_registre_commerce = models.CharField(db_column='Num_Registre_Commerce', max_length=20, blank=True, null=True,
                                             verbose_name='Numero du registre de commerce')

    objects = DeletedModelManager()
    def __str__(self):
        return  self.id



    class Meta:
        verbose_name = 'Clients'
        verbose_name_plural = 'Clients'
        app_label = 'api_sm'
        


class Sites(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    id = models.CharField(db_column='Code_site', primary_key=True, max_length=500 ,
                                 verbose_name='Code du Site')
    responsable_site = models.CharField(db_column='Responsable', max_length=500, blank=True, null=True,
                                 verbose_name='Responsable du Site')
    libelle = models.CharField(db_column='Libelle_Site', max_length=500, blank=True, null=True,
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
        return self.id


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
        app_label = 'api_sm'
        


class SituationNt(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    libelle=models.CharField(max_length=100,null=False,unique=True,verbose_name='Libelle')
    objects = DeletedModelManager()
    class Meta:
        verbose_name = 'Situation du Travail'
        verbose_name_plural = 'Situation du Travail'
        app_label = 'api_sm'
        
    def __str__(self):
        return  self.libelle
    def save(self, *args, **kwargs):
            self.libelle=self.libelle.lower()
            super(SituationNt, self).save(*args, **kwargs)





class NT(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    id=models.CharField(db_column='id',max_length=500,primary_key=True,verbose_name="id",editable=False)
    nt = models.CharField(db_column='NT', max_length=20, verbose_name='Numero du travail')
    code_site = models.ForeignKey(Sites, on_delete=models.DO_NOTHING, db_column='Code_site', null=False
                                  , verbose_name='Code du Site')
    code_client = models.ForeignKey(Clients, on_delete=models.DO_NOTHING, db_column='Code_Client',null=True
                                    , verbose_name='Code du client')
    code_situation = models.ForeignKey(SituationNt, on_delete=models.DO_NOTHING, blank=True, null=True
                                          , verbose_name='Situation')
    libelle = models.CharField(max_length=900,db_column='Libelle_NT', blank=True, null=True
                                  , verbose_name='Libelle')
    date_ouverture_nt = models.DateField(db_column='Date_Ouverture_NT', blank=True, null=True
                                         , verbose_name='Ouverture')
    date_cloture_nt = models.DateField(db_column='Date_Cloture_NT', blank=True, null=True
                                       , verbose_name='Cloture')

    objects = DeletedModelManager()

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Numero du travail'
        verbose_name_plural = 'Numero du travail'
        unique_together = (('code_site', 'nt'),)
        app_label = 'api_sm'
        





class Marche(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    id=models.CharField(max_length=500,primary_key=True,editable=False,verbose_name='Code du marché')
    nt = models.ForeignKey(NT, on_delete=models.DO_NOTHING, db_column='nt', null=False
                           , verbose_name='Numero Travail',to_field="id")


    libelle = models.CharField(null=False, max_length=500
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
    rabais =  models.DecimalField(default=0, max_digits=38, decimal_places=2, verbose_name='Rabais',
                              validators=[MinValueValidator(0), MaxValueValidator(100)], null=False)
    ht=models.DecimalField(default=0, max_digits=38, decimal_places=2,  verbose_name='Prix Hors taxe',
                              validators=[MinValueValidator(0), MaxValueValidator(100)], null=False,editable=False)
    ttc = models.DecimalField(default=0, max_digits=38, decimal_places=2, verbose_name='Prix avec taxe',
                                  validators=[MinValueValidator(0), MaxValueValidator(100)], null=False, editable=False)

    tva = models.DecimalField(default=0, max_digits=38, decimal_places=2, verbose_name='TVA',
                              validators=[MinValueValidator(0), MaxValueValidator(100)], null=False)
    rg = models.DecimalField(default=0, max_digits=38, decimal_places=2,
                              validators=[MinValueValidator(0), MaxValueValidator(100)], null=False
                                              , verbose_name='Retenue de garantie')
    code_contrat = models.CharField(null=False, blank=False, max_length=20, verbose_name='Code du contrat')
    date_signature = models.DateField(null=False, verbose_name='Date de signature')
   
    objects = DeletedModelManager()

    def __str__(self):
        return self.id

    def save_without_historical_record(self, *args, **kwargs):
        self.skip_history_when_saving = True
        try:
            ret = self.save(*args, **kwargs)
        finally:
            del self.skip_history_when_saving
        return ret

    def save_with_historical_record(self, *args, **kwargs):
        self.skip_history_when_saving = False
        try:
            ret = self.save(*args, **kwargs)
        finally:
            del self.skip_history_when_saving
        return ret


class Meta:
        verbose_name = 'Marchés'
        verbose_name_plural = 'Marchés'
        unique_together=(('nt','num_avenant'),)
        app_label = 'api_sm'
        





class DQE(SafeDeleteModel): # le prix final
    _safedelete_policy = SOFT_DELETE_CASCADE
    id=models.CharField(db_column='id',max_length=500,primary_key=True,verbose_name="id",editable=False)
    marche = models.ForeignKey(Marche,on_delete=models.DO_NOTHING,  null=False,related_name="marche_dqe",
                               to_field="id",verbose_name="Code du marché")


    code_tache = models.CharField(db_column='Code_Tache',null=False, max_length=30
                                  ,verbose_name="Code de la tache")
    libelle = models.TextField(db_column='Libelle_Tache',verbose_name="Libelle")

    unite =models.ForeignKey(TabUniteDeMesure,on_delete=models.DO_NOTHING,  null=False, verbose_name='Unité de mesure')

    est_tache_composite = models.BooleanField(db_column='Est_Tache_Composite', blank=True,
                                              null=False,default=False,verbose_name="Tache composée")
    est_tache_complementaire = models.BooleanField(db_column='Est_Tache_Complementaire', blank=True,
                                                   null=False,default=False,verbose_name="Tache complementaire")


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
        return (str(self.id))



    class Meta:
        verbose_name = 'DQE'
        verbose_name_plural = 'DQE'
        app_label = 'api_sm'
        permissions = [
            ("upload_dqe", "Can upload DQE"),
            ("download_dqe", "Can download DQE"),

        ]
        





class Ordre_De_Service(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    marche = models.ForeignKey(Marche, on_delete=models.DO_NOTHING, null=True, related_name="ods_marche")
    date_interruption = models.DateField(null=True, blank=True,verbose_name='Date Interruption')
    date_reprise = models.DateField(null=True, blank=True,verbose_name='Date Reprise')

    motif = models.TextField(null=False, blank=True,verbose_name='Motif')

    objects = DeletedModelManager()

    def save(self, *args, **kwargs):
        if(self.date_reprise and self.date_reprise):
           if (self.date_reprise > self.date_interruption):
                super(Ordre_De_Service, self).save(*args, **kwargs)
           else:
               raise  ValidationError('Date de reprise doit etre superieur à la date d\'interruption')


    class Meta:
        verbose_name = 'Ordre de service'
        verbose_name_plural = 'Ordre de service'
        app_label = 'api_sm'
        











class TypeAvance(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    libelle = models.CharField(max_length=500, null=False, unique=True)
    taux_reduction_facture=models.DecimalField(default=0, max_digits=38, decimal_places=2,
                               validators=[MinValueValidator(0), MaxValueValidator(100)], null=False)
    taux_max = models.DecimalField(default=0, max_digits=38, decimal_places=2,
                                                 validators=[MinValueValidator(0), MaxValueValidator(100)], null=False)



    objects = DeletedModelManager()

    def __str__(self):
        return self.libelle



    class Meta:
        verbose_name = 'Type Avance'
        verbose_name_plural = 'Type Avance'
        app_label = 'api_sm'
        


class Avance(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    type = models.ForeignKey(TypeAvance, on_delete=models.DO_NOTHING, null=False, to_field='id',
                             verbose_name="Type d'avance")
    num_avance = models.PositiveIntegerField(default=0, null=False, blank=True, editable=False,
                                                verbose_name="Numero d'avance")
    marche = models.ForeignKey(Marche, on_delete=models.DO_NOTHING, null=False, related_name="Avance_Marche",to_field='id')

    taux_avance = models.DecimalField(default=0, max_digits=38, decimal_places=2, verbose_name="Taux d'avance",
                                      validators=[MinValueValidator(0), MaxValueValidator(100)], null=False)

    montant = models.DecimalField(max_digits=38, decimal_places=2, validators=[MinValueValidator(0)], default=0,editable=False)


    date=models.DateField(null=False,verbose_name="Date d'avance")
    heure = models.TimeField(auto_now=True,null=False,editable=False)
    remboursee = models.BooleanField(default=False, null=False,verbose_name='Est Remboursée')


    objects = DeletedModelManager()

    def __str__(self):
        return str(self.marche)+"-"+self.type.libelle+'-'+str(self.num_avance)
    class Meta:
        verbose_name = 'Avance'
        verbose_name_plural = 'Avances'

        app_label = 'api_sm'
        





class Attachements(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    dqe = models.ForeignKey(DQE, on_delete=models.DO_NOTHING)# item + quantité marche + prix unitaire

    qte_precedente = models.DecimalField(max_digits=38, decimal_places=2, validators=[MinValueValidator(0)], default=0,
                                         editable=False,verbose_name='precedent')
    qte_mois = models.DecimalField(max_digits=38, decimal_places=2, validators=[MinValueValidator(0)], default=0,verbose_name='Quantite Mois')
    qte_cumule= models.DecimalField(max_digits=38, decimal_places=2, validators=[MinValueValidator(0)], default=0,
                                    editable=False,verbose_name='Quantite cumule')

    prix_u = models.DecimalField(max_digits=38, decimal_places=2, validators=[MinValueValidator(0)], default=0,
                                     editable=False,verbose_name='Prix unitaire')
    montant_precedent=models.DecimalField(max_digits=38, decimal_places=2, validators=[MinValueValidator(0)], default=0,
                                          editable=False,verbose_name='Montant précedent')
    montant_mois= models.DecimalField(max_digits=38, decimal_places=2, validators=[MinValueValidator(0)], default=0,verbose_name='Montant du Mois')
    montant_cumule = models.DecimalField(max_digits=38, decimal_places=2, validators=[MinValueValidator(0)], default=0,
                                         editable=False,verbose_name='Montant cumulé')
    date=models.DateField(null=False,verbose_name='Date')
    heure=models.TimeField(auto_now=True,editable=False)

    objects = DeletedModelManager()


    def __str__(self):
        return  str(self.id)+"-"+self.dqe.code_tache

    def save(self, *args, **kwargs):
        super(Attachements, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Attachements'
        verbose_name_plural = 'Attachements'
        app_label = 'api_sm'
        


class Factures(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    numero_facture=models.CharField(max_length=800,primary_key=True,verbose_name='Numero de facture')
    num_situation=models.PositiveIntegerField(default=0,null=False,blank=True,editable=False,verbose_name='Numero de situation')
    marche=models.ForeignKey(Marche,on_delete=models.DO_NOTHING,null=False,verbose_name='Marche',to_field="id")
    du = models.DateField(null=False,verbose_name='Du')
    au = models.DateField(null=False,verbose_name='Au')
    paye = models.BooleanField(default=False, null=False,editable=False)
    date = models.DateField(auto_now=True, editable=False)
    heure = models.TimeField(auto_now=True, editable=False)
    montant_precedent=models.DecimalField(max_digits=38, decimal_places=2, validators=[MinValueValidator(0)], default=0,
                                          verbose_name="Montant Precedent"
                                          ,editable=False)
    montant_mois= models.DecimalField(max_digits=38, decimal_places=2, validators=[MinValueValidator(0)], default=0,
                                      verbose_name="Montant du Mois"
                                      ,editable=False)
    montant_cumule = models.DecimalField(max_digits=38, decimal_places=2, validators=[MinValueValidator(0)], default=0,
                                         verbose_name="Montant Cumulé"
                                         ,editable=False)

    montant_rb = models.DecimalField(max_digits=38, decimal_places=2, validators=[MinValueValidator(0)], default=0,
                                       verbose_name="Montant du rabais"
                                       , editable=False) #montant du rabais du mois


    montant_rg=models.DecimalField(max_digits=38, decimal_places=2, validators=[MinValueValidator(0)], default=0,
                                         verbose_name="Montant Retenue de garantie"
                                         ,editable=False) #retenue de garantie le montant du mois


    montant_factureHT=models.DecimalField(max_digits=38, decimal_places=2, validators=[MinValueValidator(0)], default=0,
                                         verbose_name="Montant de la facture"
                                         ,editable=False)

    montant_factureTTC=models.DecimalField(max_digits=38, decimal_places=2, validators=[MinValueValidator(0)], default=0,
                                         verbose_name="Net à Payer"
                                         ,editable=False)


    objects = DeletedModelManager()



    class Meta:
        verbose_name = 'Factures'
        verbose_name_plural = 'Factures'
        app_label = 'api_sm'
        
class Remboursement(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    facture = models.ForeignKey(Factures, on_delete=models.DO_NOTHING, null=True, blank=True, to_field="numero_facture")
    avance=models.ForeignKey(Avance, on_delete=models.DO_NOTHING, null=True, blank=True)

    montant_mois =models.DecimalField(max_digits=38, decimal_places=2, validators=[MinValueValidator(0)], default=0,
                                         verbose_name="Montant Mois"
                                         ,editable=False)
    montant_cumule=models.DecimalField(max_digits=38, decimal_places=2, validators=[MinValueValidator(0)], default=0,
                                         verbose_name="Montant Cumule"
                                         ,editable=False)
    rst_remb=models.DecimalField(max_digits=38, decimal_places=2, validators=[MinValueValidator(0)], default=0,
                                         verbose_name="Reste à rembourser"
                                         ,editable=False)

    date=models.DateField(auto_now=True,null=False,editable=False)
    heure=models.TimeField(auto_now=True,null=False,editable=False)

    objects = DeletedModelManager()



    class Meta:
        verbose_name = 'Remboursement'
        verbose_name_plural = 'Remboursements'
        app_label = 'api_sm'



class DetailFacture(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    facture=models.ForeignKey(Factures,on_delete=models.DO_NOTHING,null=True,blank=True,to_field="numero_facture")
    detail=models.ForeignKey(Attachements,on_delete=models.DO_NOTHING)
    objects = DeletedModelManager()

    class Meta:
        verbose_name = 'Datails Facture'
        verbose_name_plural = 'Details Facture'
        app_label = 'api_sm'
        


class ModePaiement(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    libelle=models.CharField(max_length=500,null=False,unique=True)

    def __str__(self):
        return  self.libelle
    class Meta:
        verbose_name = 'Mode de Paiement'
        verbose_name_plural = 'Mode de Paiement'
        app_label = 'api_sm'
        



class Encaissement(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    facture=models.ForeignKey(Factures,on_delete=models.DO_NOTHING,null=False,blank=True,verbose_name="Facture")
    date_encaissement=models.DateField(null=False,verbose_name="Date d'encaissement")
    mode_paiement=models.ForeignKey(ModePaiement,on_delete=models.DO_NOTHING,null=False,blank=True,verbose_name="Mode de paiement")
    montant_encaisse=models.DecimalField(max_digits=38, decimal_places=2, blank=True,verbose_name="Montant encaissé",
                                     validators=[MinValueValidator(0)], default=0)
    montant_creance = models.DecimalField(max_digits=38, decimal_places=2, blank=True,verbose_name="Montant en créance",
                                           validators=[MinValueValidator(0)], default=0,editable=False)
    agence =models.CharField(db_column='Code_Agence', null=False, max_length=15)
    numero_piece = models.CharField(max_length=300,null=False,verbose_name="Numero de piéce")
    objects = DeletedModelManager()


    def save(self, *args, **kwargs):
        sum = Encaissement.objects.filter(facture=self.facture).aggregate(models.Sum('montant_encaisse'))[
            "montant_encaisse__sum"]
        if(sum==None):
            sum=0
        sum=sum+self.montant_encaisse
        self.montant_creance = round(self.facture.montant_factureTTC - sum,2)
        if(self.montant_creance == 0):
            self.facture.paye=True
            self.facture.save()
        if(self.montant_creance >= 0):
            super(Encaissement, self).save(*args, **kwargs)
        else:
            raise ValidationError('Le paiement de la facture est terminer')



    class Meta:
        verbose_name = 'Encaissement'
        verbose_name_plural = 'Encaissement'
        unique_together=(("facture","date_encaissement"),)
        app_label = 'api_sm'



class TypeCaution(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    libelle = models.CharField(max_length=500,null=True,blank=True)
    type_avance = models.ForeignKey(TypeAvance, on_delete=models.DO_NOTHING, null=True,blank=True, to_field='id',
                             verbose_name="Type d'avance")
    taux_exact= models.DecimalField(max_digits=38, decimal_places=2,
                                   validators=[MinValueValidator(0), MaxValueValidator(100)], null=True,blank=True)
    taux_min = models.DecimalField(max_digits=38, decimal_places=2,
                               validators=[MinValueValidator(0), MaxValueValidator(100)], null=True,blank=True)
    taux_max = models.DecimalField( max_digits=38, decimal_places=2,
                                   validators=[MinValueValidator(0), MaxValueValidator(100)], null=True,blank=True)

    objects = DeletedModelManager()

    def __str__(self):
        return self.libelle

    def save(self, *args, **kwargs):
        super(TypeCaution, self).save(*args, **kwargs)



    class Meta:
        verbose_name = 'Type_Caution'
        verbose_name_plural = 'Type_Caution'
        app_label = 'api_sm'


class Cautions(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    marche = models.ForeignKey(Marche, on_delete=models.DO_NOTHING, null=False, related_name="Caution_Marche")
    type = models.ForeignKey(TypeCaution, on_delete=models.DO_NOTHING, null=False)
    avance = models.ForeignKey(Avance, on_delete=models.DO_NOTHING, null=True, blank=True)
    date_soumission = models.DateField(null=False,verbose_name="Date dépot")
    taux = models.DecimalField(default=0,max_digits=38, decimal_places=2,
                                     validators=[MinValueValidator(0), MaxValueValidator(100)], null=False)
    agence =models.CharField(db_column='Code_Agence', null=False, max_length=15)
    montant = models.DecimalField(
        max_digits=38, decimal_places=2,
        validators=[MinValueValidator(0)], default=0,
        editable=False
    )
    est_recupere = models.BooleanField(default=True, null=False, editable=False)

    objects = DeletedModelManager()



    class Meta:
        verbose_name = 'Caution'
        verbose_name_plural = 'Caution'
        app_label = 'api_sm'




