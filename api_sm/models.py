from django.db import models
from colorfield.fields import ColorField

# Create your models here.
class Interface_de_Connexion(models.Model):
    key = models.BigAutoField(primary_key=True)
    src=models.ImageField(upload_to="Images/Login",null=False,blank=True,default='default.png')
    text=models.CharField(max_length=100,null=True,blank=True)
    caption=models.CharField(max_length=100,null=True,blank=True)
    color=ColorField(null=True,blank=True,format="rgba",default="transparent")
    visible=models.BooleanField(default=True)
    def delete(self, *args, **kwargs):
        self.visible=False
        super(Interface_de_Connexion, self).save(*args, **kwargs)
