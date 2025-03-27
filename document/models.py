from django.db import models

from user.models import User

class Documents(models.Model):
    title =models.CharField(max_length=125,verbose_name="Receipts number")
    amount=models.IntegerField(verbose_name='Amount paid')
    description=models.CharField(max_length=250,verbose_name='Description about product')
    user=models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user upload')
    sender=models.CharField(max_length=100,verbose_name='who brought product')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Times stored')
    
    def __str__(self):
        return f'{self.title} ({self.amount},{self.description})'
