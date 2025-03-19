from django.db import models

from user.models import User

class Shop(models.Model):
    name =models.CharField(max_length=200)
    user =models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='user assign to shop')
