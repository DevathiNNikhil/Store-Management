from django.db import models

# Create your models here.
class data(models.Model):
    date=models.CharField(max_length=50)
    product=models.IntegerField()
    sales=models.IntegerField()
    def __str__(self):
        return self.product