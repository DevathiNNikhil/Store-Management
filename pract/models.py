from django.db import models
from django.db.models.fields.related import ForeignKey

# Create your models here.
class bill1(models.Model):
    product=models.CharField(max_length=20)
    qty=models.IntegerField()
    price=models.IntegerField()
    def __str__(self):
        return self.product
class products(models.Model):
    product=models.CharField(max_length=20)
    qty=models.IntegerField()
    unique=models.IntegerField(primary_key=True)
    buy_price=models.IntegerField()
    sell_price=models.IntegerField()
    def __str__(self):
        return self.product
class sales(models.Model):
    product=models.CharField(max_length=20)
    qty=models.IntegerField()
    buy_price=models.IntegerField()
    sell_price=models.IntegerField()
    def __str__(self):
        return self.product

class bill(models.Model):
    date1=models.CharField(max_length=20)
    product=models.ForeignKey(products,on_delete=models.CASCADE)
    sales1=models.IntegerField()
    def __str__(self):
        return str(self.product)

    
