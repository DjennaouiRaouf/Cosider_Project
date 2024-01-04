# signals.py
import sys
from datetime import datetime

from django.db.models import Q
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

@receiver(post_softdelete, sender=Factures)
def update_on_softdelete(sender, instance, **kwargs):
    pass

@receiver(pre_save, sender=DetailFacture)
def pre_save_detail_facture(sender, instance, **kwargs):
    if(instance.detail.dqe.marche != instance.facture.marche):
        raise ValidationError("Cette attachement ne fais pas partie du marche")

@receiver(pre_save, sender=Avance)
def pre_save_avance(sender, instance, **kwargs):
    if(instance.marche.nt.code_client.id != instance.client.id):
        raise ValidationError("Ce client ne fais pas partie du marche")















