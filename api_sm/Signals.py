# signals.py
import sys
from datetime import datetime

from _decimal import Decimal
from django.db import IntegrityError
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
    if (instance.date_cloture_nt and instance.date_ouverture_nt):
        if (instance.date_cloture_nt <= instance.date_ouverture_nt):
            raise ValidationError("Date de cloture doit etre supérieur ou égale à la date d\'ouverture")


@receiver(post_save, sender=NT)
def post_save_nt(sender, instance, created, **kwargs):
    if created:
        instance.id = instance.code_site.id + "-" + instance.nt
        if (instance.date_cloture_nt and instance.date_ouverture_nt):
            if (instance.date_cloture_nt <= instance.date_ouverture_nt):
                raise ValidationError("Date de cloture doit etre supérieur ou égale à la date d\'ouverture")

    if not created:
        if (instance.date_cloture_nt and instance.date_ouverture_nt):
            if (instance.date_cloture_nt <= instance.date_ouverture_nt):
                raise ValidationError("Date de cloture doit etre supérieur ou égale à la date d\'ouverture")


# DQE

@receiver(pre_save, sender=DQE)
def pre_save_dqe(sender, instance, **kwargs):
    if not instance.pk:
        instance.id = str(instance.code_tache) + "_" + str(instance.marche.id)

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
        instance.id = str(instance.code_tache) + "_" + str(instance.marche.id)

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

    qte_dqe = DQE.objects.filter(Q(marche=instance.marche)).aggregate(
        models.Sum('quantite'))["quantite__sum"]

    try:
        factures = Factures.objects.filter(marche=instance.marche)
        for facture in factures:
            qte_real = Attachements.objects.filter(Q(dqe__marche=instance.marche) & Q(date__lte=facture.au)).aggregate(
                models.Sum('qte_mois'))["qte_mois__sum"]
            facture.taux_realise = round((qte_real / qte_dqe) * 100, 2)
            facture.save()

    except Factures.DoesNotExist :
        pass

# marche


@receiver(post_save, sender=Marche)
def post_save_marche(sender, instance, created, **kwargs):
    total = DQE.objects.filter(marche=instance).aggregate(models.Sum('prix_q'))[
        "prix_q__sum"]
    if not total:
        total = 0

    Marche.objects.filter(id=instance.pk).update(
        ht=round(total, 2),
        ttc=round(total + (total * instance.tva / 100), 2))


"""
@receiver(pre_create_historical_record,sender=Marche)
def pre_create_historical_record_callback(sender, **kwargs):
    instance = kwargs['instance']
    sender_model_name = sender.__name__
    if(sender_model_name == "HistoricalMarche"):
        try:
            latest_history_record = instance.history.latest()
            print(latest_history_record.date_signature,instance.date_signature)
            if latest_history_record.date_signature == instance.date_signature:
                raise IntegrityError("Data is already present in the historical records.")
            else:
                print(instance.history.num_avenant)
        except Marche.history.model.DoesNotExist:
            pass
    else:
        pass
"""


@receiver(pre_save, sender=Attachements)
def pre_save_attachements(sender, instance, **kwargs):
    if not instance.pk:
        attachements = Attachements.objects.filter(~Q(pk=instance.pk) & Q(dqe=instance.dqe))
        instance.prix_u = instance.dqe.prix_u
        prix_u = instance.dqe.prix_u
        if (attachements):  # courant
            previous = attachements.latest('date', 'id')
            instance.qte_precedente = previous.qte_cumule
            instance.qte_cumule = instance.qte_precedente + instance.qte_mois
            instance.montant_precedent = round(previous.montant_cumule, 2)
            instance.montant_mois = round(instance.qte_mois * prix_u, 2)
            instance.montant_cumule = round(instance.montant_precedent + instance.montant_mois, 2)

        else:  # debut
            instance.qte_precedente = 0
            instance.qte_cumule = instance.qte_mois
            instance.montant_precedent = 0
            instance.montant_mois = instance.qte_mois * prix_u
            instance.montant_cumule = round(instance.montant_precedent + instance.montant_mois, 2)



@receiver(pre_save, sender=Factures)
def pre_save_factures(sender, instance, **kwargs):
    if (instance.du > instance.au):
        raise ValidationError('Date de debut doit etre inferieur à la date de fin')
    else:
        debut = instance.du
        fin = instance.au
        if( not Attachements.objects.filter(dqe__marche=instance.marche, date__lte=fin, date__gte=debut)):
            raise ValidationError('Facturation impossible les attachements ne sont pas disponible ')

        sum = Attachements.objects.filter(dqe__marche=instance.marche, date__lte=fin, date__gte=debut).aggregate(
            models.Sum('montant_precedent'),
            models.Sum('montant_mois'),
            models.Sum('montant_cumule'))

        mm = sum["montant_mois__sum"]
        mp = sum["montant_precedent__sum"]
        mc = sum["montant_cumule__sum"]

        instance.montant_precedent = mp
        instance.montant_mois = mm
        instance.montant_cumule = mc
        instance.montant_rb = mm * (instance.marche.rabais / 100)
        instance.montant_rg = round((mm - instance.montant_rb) * (instance.marche.rg / 100), 2)
        instance.montant_factureHT = round(instance.montant_mois - instance.montant_rb - instance.montant_rg, 2)
        instance.montant_factureTTC = round(
        instance.montant_factureHT + (instance.montant_factureHT * instance.marche.tva / 100), 2)
        qte_real = Attachements.objects.filter(Q(dqe__marche=instance.marche) & Q(date__lte=fin)).aggregate(
                models.Sum('qte_mois'))["qte_mois__sum"]
        qte_dqe = DQE.objects.filter(Q(marche=instance.marche)).aggregate(
                models.Sum('quantite'))["quantite__sum"]
        instance.taux_realise = round((qte_real / qte_dqe) * 100, 2)

    if instance.pk:
        instance.montant_factureHT=round(instance.montant_factureHT-instance.montant_avf_remb-instance.montant_ava_remb,2)
        instance.montant_factureTTC = round(
            instance.montant_factureHT + (instance.montant_factureHT * instance.marche.tva / 100), 2)


@receiver(pre_save, sender=Encaissement)
def pre_save_encaissement(sender, instance, **kwargs):
    try:
        sum = Encaissement.objects.filter(facture=instance.facture).aggregate(models.Sum('montant_encaisse'))[
                "montant_encaisse__sum"]
    except Encaissement.DoesNotExist:
            sum=0
    sum=sum+instance.montant_encaisse
    instance.montant_creance = round(instance.facture.montant_factureTTC - sum,2)
    if(instance.montant_creance == 0):
        instance.facture.paye=True
        instance.facture.save()
    if(instance.montant_creance < 0):
        raise ValidationError('Le paiement de la facture est terminer')

@receiver(pre_save, sender=Remboursement)
def pre_save_remboursement(sender, instance, **kwargs):

    if not instance.pk:
        if (instance.avance.remboursee):
            raise ValidationError('Cette avance est remboursée')

        elif (Decimal(instance.avance.fin) < Decimal(instance.facture.taux_realise)):
            raise ValidationError('Cette avance peut pas etre emboursé dans cette situation')

        else:
            remb = Remboursement.objects.filter(
                Q(facture__num_situation__lt=instance.facture.num_situation) & Q(avance__type=instance.avance.type.id) & Q(avance__num_avance=instance.avance.num_avance)
            & Q(avance__remboursee=False))

            if (remb):  # courant
                previous = remb.last()
                print(previous)
                tremb=round((instance.avance.taux_avance/(instance.avance.fin-instance.facture.taux_realise))*100,2)
                mm = (instance.facture.montant_mois - instance.facture.montant_rb - instance.facture.montant_rg-instance.facture.montant_avf_remb-instance.facture.montant_ava_remb) * (
                        tremb / 100)

                cumule = mm + previous.montant_cumule
                rar = instance.avance.montant - cumule
                print()
                if (rar < 0):
                    instance.montant_mois = previous.rst_remb
                    instance.montant_cumule = instance.montant_mois + previous.montant_cumule
                    instance.rst_remb = instance.avance.montant - instance.montant_cumule

                else:
                    instance.montant_mois = mm
                    instance.montant_cumule = cumule
                    instance.rst_remb = rar

                if instance.avance.type.id == 1:
                    instance.facture.montant_avf_remb = round(instance.montant_mois, 2)

                if instance.avance.type.id == 2:
                    instance.facture.montant_ava_remb = round(instance.montant_mois, 2)
                instance.facture.save()

                if (instance.rst_remb == 0):
                    instance.avance.remboursee=True
                    instance.avance.save()

            else:  # debut pas de precedent
                tremb = round(
                    (instance.avance.taux_avance / (instance.avance.fin - instance.facture.taux_realise)) * 100, 2)
                mm = (instance.facture.montant_mois - instance.facture.montant_rb - instance.facture.montant_rg-instance.facture.montant_avf_remb-instance.facture.montant_ava_remb) * (
                        tremb / 100)
                cumule = mm
                rar = instance.avance.montant - cumule
                if (rar < 0):
                    instance.montant_mois = instance.avance.montant
                    instance.montant_cumule = instance.montant_mois
                    instance.rst_remb = instance.avance.montant - instance.montant_cumule
                else:
                    instance.montant_mois = mm
                    instance.montant_cumule = cumule
                    instance.rst_remb = rar

                if instance.avance.type.id == 1:
                    instance.facture.montant_avf_remb = round(instance.montant_mois, 2)
                if instance.avance.type.id == 2:
                    instance.facture.montant_ava_remb = round(instance.montant_mois, 2)
                instance.facture.save()
                if (instance.rst_remb == 0):
                    instance.avance.remboursee = True
                    instance.avance.save()


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




@receiver(post_softdelete, sender=Factures)
def update_on_softdelete(sender, instance, **kwargs):
    count = Factures.deleted_objects.filter(numero_facture__startswith=f'C-{instance.pk}').count()
    print(count)
    num_f = 'C-' + instance.pk + '-' + str(count)
    num_sit = (-1) * (instance.num_situation)
    DetailFacture.objects.filter(facture=instance.pk).update(facture=None)
    Remboursement.objects.filter(facture=instance.pk).update(facture=None)
    Factures.objects.filter(numero_facture=instance.pk).update(numero_facture=num_f, num_situation=num_sit)
    DetailFacture.objects.filter(facture=None).update(facture=num_f)
    Remboursement.objects.filter(facture=None).update(facture=num_f)
    DetailFacture.objects.filter(facture=num_f).delete()
    Remboursement.objects.filter(facture=num_f).delete()


@receiver(pre_save, sender=DetailFacture)
def pre_save_detail_facture(sender, instance, **kwargs):
    if (instance.detail.dqe.marche != instance.facture.marche):
        raise ValidationError("Cette attachement ne fais pas partie du marche")


@receiver(pre_save, sender=Avance)
def pre_save_avance(sender, instance, **kwargs):
    if not instance.pk:
        instance.taux_avance = round((instance.montant / instance.marche.ttc)*100, 2)
        print(instance.taux_avance)
        if (instance.type.id == 1 and instance.taux_avance > instance.type.taux_max):
            raise ValidationError(
                f'L\'avance de type {instance.type.libelle} ne doit pas dépassé le taux   {instance.type.taux_max}%')

        if (instance.type.id != 1 and instance.taux_avance > instance.type.taux_max):
            raise ValidationError(
                f'Vous avez une avance de type Avance {instance.type.libelle} la somme des taux ne doit pas dépasser {instance.type.taux_max}%')


        instance.num_avance = Avance.objects.filter(marche=instance.marche).count()





@receiver(post_save, sender=Avance)
def post_save_avance(sender, instance, created, **kwargs):
    if(created):
        if (not instance.deleted):
            sum = Avance.objects.filter(marche=instance.marche, type=instance.type).aggregate(models.Sum('taux_avance'))[
                "taux_avance__sum"]

            if (instance.type.id != 1 and sum > instance.type.taux_max):
                raise ValidationError(
                    f'Vous avez plusieurs avances de type Avance {instance.type.libelle} la somme des taux ne doit pas dépasser {instance.type.taux_max}%')

            if (instance.type.id == 1 and (instance.taux_avance  >  instance.type.taux_max or sum > instance.type.taux_max)):
                raise ValidationError(
                    f'L\'avance de type {instance.type.libelle} doit etre égale  {instance.type.taux_max}%')





@receiver(pre_save, sender=TypeCaution)
def pre_save_type_caution(sender, instance, **kwargs):
    if (instance.type_avance):
        instance.libelle = instance.type_avance.libelle
    if (not instance.type_avance and not instance.libelle):
        raise ValidationError(
            f'Libelle de la caution est obligatoire')
    if (not instance.taux_exact and not instance.taux_min and not instance.taux_max):
        raise ValidationError(
            f'Le taux de la caution doit etre soit une valeur exact ou intervale')

    if ((instance.taux_exact and instance.taux_min) or (instance.taux_exact and instance.taux_max)):
        raise ValidationError(
            f'Le taux de la caution doit etre soit une valeur exact ou intervale')

    if (instance.taux_min and not instance.taux_max):
        raise ValidationError(
            f'Le taux  MAX de la caution est obligatoir')

    if (not instance.taux_min and instance.taux_max):
        instance.taux_min = 0

    if (instance.taux_min and instance.taux_max):
        if (instance.taux_min >= instance.taux_max):
            raise ValidationError(
                f'Le taux  MIN de la caution  doit etre supérieur au taux MAX')


@receiver(pre_save, sender=Cautions)
def pre_save_caution(sender, instance, **kwargs):
    if (instance.avance):
        if (instance.avance.marche != instance.marche):
            raise ValidationError(
                f'Le Marché {instance.marche} ne posséde pas cette avance  de type {instance.avance.type}')
        else:
            if (instance.avance.type != instance.type.type_avance):
                raise ValidationError(
                    f'Cette avance est de type {instance.avance.type} n\'est pas compatible avec la caution de type {instance.type.type_avance} ')

    exact = instance.type.taux_exact
    max = instance.type.taux_max
    min = instance.type.taux_min
    if (exact != None):
        if (instance.taux != exact):
            raise ValidationError(
                f'le taux de la caution du marché  {instance.taux} doit etre égale à {exact}')

        if (min != None and max != None):
            if (not min <= instance.taux <= max):
                raise ValidationError(
                    f'le taux de la caution du marché  {instance.taux}  doit etre comprise entre [{min},{max}]')

    montant = 0
    if (instance.avance):
        montant = instance.avance.montant
    else:
        montant = instance.marche.ttc

    instance.montant = round(montant * instance.taux / 100, 2)




