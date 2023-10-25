from django.db import models
from colorfield.fields import ColorField

# Create your models here.
class Images(models.Model):
    key = models.BigAutoField(primary_key=True)
    src=models.ImageField(upload_to="Images/Login",null=False,blank=True,default='default.png')
    text=models.CharField(max_length=100,null=True,blank=True)
    caption=models.CharField(max_length=100,null=True,blank=True)
    color=ColorField(null=True,blank=True,format="rgba",default="transparent")
    visible=models.BooleanField(default=True)
    def delete(self, *args, **kwargs):
        self.visible=False
        super(Images, self).save(*args, **kwargs)
