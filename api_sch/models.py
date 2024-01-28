from django.db import models


from django.db import models


class TabProduction(models.Model):
    id_production = models.AutoField(db_column='ID_Production', primary_key=True,verbose_name='ID')
    code_type_production = models.CharField(max_length=2,null=False, db_column='Code_Type_Production',verbose_name='Type Production')
    code_site = models.CharField(max_length=500,null=False, db_column='Code_site',verbose_name='Code Site')
    code_filiale = models.CharField(db_column='Code_Filiale', max_length=5, blank=True, null=True,verbose_name='Code Filiale')
    nt = models.CharField(max_length=4, db_column='NT',  blank=True, null=True,verbose_name='NT')
    code_groupeactivite = models.CharField(max_length=4, db_column='Code_GroupeActivite',blank=True, null=True)
    code_activite = models.CharField(max_length=4, db_column='Code_Activite', blank=True, null=True)
    code_tache = models.CharField(max_length=4, db_column='Code_Tache', blank=True, null=True)
    recepteur = models.CharField(db_column='Recepteur', max_length=20, blank=True, null=True)
    code_produit = models.CharField(max_length=4, db_column='Code_Produit', blank=True, null=True)
    code_unite_mesure = models.CharField(max_length=4, db_column='Code_Unite_Mesure', blank=True, null=True,verbose_name='Unite')
    type_prestation = models.SmallIntegerField(db_column='Type_Prestation', blank=True, null=True,verbose_name='Type Prestation')
    mmaa = models.DateField(db_column='Mmaa')
    quantite_1 = models.FloatField(db_column='Quantite_1', blank=True, null=True)
    valeur_1 = models.DecimalField(db_column='Valeur_1', max_digits=19, decimal_places=4, blank=True, null=True)
    quantite_2 = models.FloatField(db_column='Quantite_2', blank=True, null=True)
    valeur_2 = models.DecimalField(db_column='Valeur_2', max_digits=19, decimal_places=4, blank=True, null=True)
    quantite_3 = models.FloatField(db_column='Quantite_3', blank=True, null=True)
    valeur_3 = models.DecimalField(db_column='Valeur_3', max_digits=19, decimal_places=4, blank=True, null=True)
    prevu_realiser = models.CharField(db_column='Prevu_Realiser', max_length=1)
    est_cloturer = models.BooleanField(db_column='Est_Cloturer', blank=True, null=True)
    user_id = models.CharField(db_column='User_ID', max_length=15, blank=True, null=True)
    date_modification = models.DateTimeField(db_column='Date_Modification', blank=True, null=True)

    class Meta:
        db_table = 'Tab_Production'
        app_label = 'api_sch'


