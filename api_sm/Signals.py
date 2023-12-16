# signals.py
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import *


# NT
@receiver(pre_save, sender=NT)
def pre_save_nt(sender, instance, **kwargs):
    if not instance.pk:
        instance.id = instance.code_site.code_site+"-"+instance.nt

    if (instance.date_cloture_nt <= instance.date_ouverture_nt):
        raise ValidationError("Date de cloture doit etre supérieur ou égale à la date d\'ouverture")


@receiver(post_save, sender=NT)
def post_save_nt(sender, instance, created, **kwargs):
    if created:
        instance.id = instance.code_site.code_site+"-" + instance.nt

        if (instance.date_cloture_nt <= instance.date_ouverture_nt):
            raise ValidationError("Date de cloture doit etre supérieur ou égale à la date d\'ouverture")

    if not created:
        if (instance.date_cloture_nt <= instance.date_ouverture_nt):
            raise ValidationError("Date de cloture doit etre supérieur ou égale à la date d\'ouverture")


#DQE

@receiver(pre_save, sender=DQE)
def pre_save_dqe(sender, instance, **kwargs):
    instance.designation = instance.designation.lower()
    try:
        old_instance = DQE.objects.get(pk=instance.pk)
    except DQE.DoesNotExist:
        old_instance = None

    if old_instance and not old_instance.marche.revisable: # bloquer la modification du prix_u en cas ou le contrat ne soit pas révisable
        instance.prix_u = old_instance.prix_u

    instance.prix_q = round(instance.quantite * instance.prix_u, 2)

pre_save.connect(pre_save_dqe, sender=DQE)

@receiver(post_save, sender=DQE)
def post_save_dqe(sender, instance, created, **kwargs):
    #mise a jour du prix dans  le contrat
    total = DQE.objects.filter(marche=instance.marche).aggregate(models.Sum('prix_q'))[
                "prix_q__sum"]
    instance.marche.ht=round(total,2)
    instance.marche.ttc= round(total + (total * instance.marche.tva / 100), 2)
    instance.marche.num_avenant=instance.marche.num_avenant
    instance.marche.save()


#marche
@receiver(pre_save, sender=Marche)
def pre_save_marche(sender, instance, **kwargs):
    if not instance.pk:
        instance.num_avenant = Marche.objects.filter(nt=instance.nt).count()
        instance.id = str(instance.nt.id) + "-" + str(instance.num_avenant)



@receiver(pre_save, sender=Attachements)
def pre_save_attachements(sender, instance, **kwargs):
    attachements=Attachements.objects.filter(pk=instance.pk)
    instance.qte_precedente=instance.qte_cumule
    instance.qte_mois+=instance.qte_cumule










