from django.db import models
from colorfield.fields import ColorField

# Create your models here.
class Images(models.Model):
    key = models.BigAutoField(primary_key=True)
    src=models.ImageField(upload_to="Images/Login",null=False,blank=True,default='default.png')
    visible=models.BooleanField(default=True)
    def delete(self, *args, **kwargs):
        self.visible=False
        super(Images, self).save(*args, **kwargs)
    class Meta:
        verbose_name = 'Images'
        verbose_name_plural = 'Images'

