# signals.py
import sys
from datetime import datetime

from django.db.models import Q, Count
from django.db.models.signals import post_save, pre_save, post_delete, pre_delete
from django.dispatch import *
from num2words import num2words
from safedelete.signals import post_softdelete, pre_softdelete
from simple_history import register
from simple_history.signals import pre_create_historical_record
from .models import *


# NT
@receiver(pre_save, sender=NT)
def pre_save_nt(sender, instance, **kwargs):
    if not instance.pk:
        instance.id = instance.code_site.id + "-" + instance.nt

    if (instance.date_cloture_nt <= instance.date_ouverture_nt):
        raise ValidationError("Date de cloture doit etre supérieur ou égale à la date d\'ouverture")


@receiver(post_save, sender=NT)
def post_save_nt(sender, instance, created, **kwargs):
    if created:
        instance.id = instance.code_site.id + "-" + instance.nt

        if (instance.date_cloture_nt <= instance.date_ouverture_nt):
            raise ValidationError("Date de cloture doit etre supérieur ou égale à la date d\'ouverture")

    if not created:
        if (instance.date_cloture_nt <= instance.date_ouverture_nt):
            raise ValidationError("Date de cloture doit etre supérieur ou égale à la date d\'ouverture")


# DQE

@receiver(pre_save, sender=DQE)
def pre_save_dqe(sender, instance, **kwargs):
    if not instance.pk:
        instance.id = instance.marche.id + "-" + instance.code_tache

    instance.libelle = instance.libelle.lower()

    try:
        old_instance = DQE.objects.get(pk=instance.pk)
    except DQE.DoesNotExist:
        old_instance = None

    if old_instance and not old_instance.marche.revisable:  # bloquer la modification du prix_u en cas ou le contrat ne soit pas révisable
        instance.prix_u = old_instance.prix_u

    instance.prix_q = round(instance.quantite * instance.prix_u, 2)


@receiver(post_save, sender=DQE)
def post_save_dqe(sender, instance, created, **kwargs):
    if created:
        instance.id = instance.marche.id + "-" + instance.code_tache
        total = DQE.objects.filter(marche=instance.marche).aggregate(models.Sum('prix_q'))[
            "prix_q__sum"]
        if not total:
            total = 0
        instance.marche.ht = round(total, 2)
        instance.marche.ttc = round(total + (total * instance.marche.tva / 100), 2)
        instance.marche.save()

    if not created:

        instance.id = instance.marche.id + "-" + instance.code_tache
        total = DQE.objects.filter(marche=instance.marche).aggregate(models.Sum('prix_q'))[
            "prix_q__sum"]
        if not total:
            total = 0
        instance.marche.ht = round(total, 2)
        instance.marche.ttc = round(total + (total * instance.marche.tva / 100), 2)
        instance.marche.save()

# marche
@receiver(pre_save, sender=Marche)
def pre_save_marche(sender, instance, **kwargs):
    instance.id = str(instance.nt.id)


# attechements (décompte provisoir)

@receiver(pre_save, sender=Attachements)
def pre_save_attachements(sender, instance, **kwargs):

    attachements = Attachements.objects.filter(~Q(pk=instance.pk) & Q(dqe=instance.dqe))
    instance.prix_u = instance.dqe.prix_u
    prix_u=instance.dqe.prix_u
    if (attachements):  # courant
        previous = attachements.latest('date','heure')
        instance.qte_precedente = previous.qte_cumule
        instance.qte_cumule = instance.qte_precedente + instance.qte_mois
        instance.montant_precedent = round(previous.montant_cumule,2)
        instance.montant_mois = round(instance.qte_mois * prix_u,2)
        instance.montant_cumule = round(instance.montant_precedent+instance.montant_mois,2)
    else:  # debut
        instance.qte_precedente = 0
        instance.qte_cumule = instance.qte_mois
        instance.montant_precedent = 0
        instance.montant_mois = instance.qte_mois * prix_u
        instance.montant_cumule = round(instance.montant_precedent+instance.montant_mois,2)





@receiver(pre_save, sender=Factures)
def pre_save_factures(sender, instance, **kwargs):
    if(instance.du > instance.au):
        raise ValidationError('Date de debut doit etre inferieur à la date de fin')
    else:
        debut = instance.du
        fin = instance.au
        sum = Attachements.objects.filter(dqe__marche=instance.marche, date__lte=fin, date__gte=debut).aggregate(
            models.Sum('montant_precedent'),
            models.Sum('montant_mois'),
            models.Sum('montant_cumule'))
        mm=sum["montant_mois__sum"]
        mp=sum["montant_precedent__sum"]
        mc=sum["montant_cumule__sum"]
        instance.montant_precedent = mp
        instance.montant_mois = mm
        instance.montant_cumule = mc

        instance.montant_rg= mm * (instance.marche.rg/100)
        instance.montant_taxe = mm * (instance.marche.tva / 100)
        instance.montant_rb = mm * (instance.marche.rabais / 100)

        instance.a_payer=mm-instance.montant_rg-instance.montant_rb+instance.montant_taxe



@receiver(pre_save, sender=ModePaiement)
def pre_save_mp(sender, instance, **kwargs):
    instance.libelle = instance.libelle.lower()





@receiver(post_save, sender=Factures)
def post_save_facture(sender, instance, created, **kwargs):
    if created:
        debut = instance.du
        fin = instance.au
        details = Attachements.objects.filter(dqe__marche=instance.marche, date__lte=fin, date__gte=debut)
        for d in details:
            DetailFacture(
                facture=instance,
                detail=d
            ).save()
        instance.num_situation = Factures.objects.filter(marche=instance.marche).count()
        avance=Avance.objects.get(Q(marche=instance.marche) & Q(client=instance.marche.nt.code_client) & Q(date__range=[instance.du,instance.au] ))
        Remboursement.objects.create(facture=instance,avance=avance)
        instance.save()



@receiver(pre_save, sender=Remboursement)
def pre_save_remboursement(sender, instance, **kwargs):
    if not instance.pk:
        instance.montant_precedent=0
        instance.montant_mois=round(instance.facture.montant_mois*instance.avance.type.taux_reduction_facture/100,2)
        instance.montant_cumule=round(instance.facture.montant_mois*instance.avance.type.taux_reduction_facture/100,2)
        instance.rst_remb=round(instance.avance.montant-instance.montant_cumule,2)




@receiver(post_save, sender=Remboursement)
def post_save_remboursement(sender, instance, created, **kwargs):


    pass

@receiver(post_softdelete, sender=Factures)
def update_on_softdelete(sender, instance, **kwargs):
    count=Factures.objects.filter(numero_facture=f'C-{instance.pk}').count()
    if(count==None):
        count=0

    num_f='C-'+instance.pk+'-'+str(count)
    DetailFacture.objects.filter(facture=instance.pk).update(facture=None)
    Factures.objects.filter(numero_facture=instance.pk).update(numero_facture=num_f)
    DetailFacture.objects.filter(facture=None).update(facture=num_f)

@receiver(pre_save, sender=DetailFacture)
def pre_save_detail_facture(sender, instance, **kwargs):
    if(instance.detail.dqe.marche != instance.facture.marche):
        raise ValidationError("Cette attachement ne fais pas partie du marche")


@receiver(pre_save, sender=Avance)
def pre_save_avance(sender, instance, **kwargs):

    if(instance.marche.nt.code_client.id != instance.client.id):
        raise ValidationError("Ce client ne fais pas partie du marche")
    instance.montant= round((instance.marche.ttc)*instance.taux_avance/100,2)
    if (instance.taux_avance > instance.type.taux_max):
        raise ValidationError(
            f'Vous avez une avance de type Avance {instance.type.libelle} la somme des taux ne doit pas dépasser {instance.type.taux_max}%')



@receiver(post_save, sender=Avance)
def post_save_avance(sender, instance, created, **kwargs):
    sum = Avance.objects.filter(marche=instance.marche, type=instance.type).aggregate(models.Sum('taux_avance'))[
        "taux_avance__sum"]
    if (sum > instance.type.taux_max):
        raise ValidationError(
            f'Vous avez plusieurs avances de type Avance {instance.type.libelle} la somme des taux ne doit pas dépasser {instance.type.taux_max}%')

















