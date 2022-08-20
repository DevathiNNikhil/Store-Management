from django.db import models

# Create your models here.
class form(models.Model):
    product=models.CharField(max_length=20)
    qty=models.IntegerField()
    def __str__(self):
        return product
