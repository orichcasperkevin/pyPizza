from django.db import models

# Create your models here.
class Crust(models.Model):
    SIZES = [
        ('SMALL', 1),
        ('MEDIUM', 2),
        ('LARGE', 3),
        ('XLARGE', 4)
    ]
    size = models.IntegerField(choices=SIZES)
    price = models.DecimalField(max_digits=5,decimal_places=2)

class Topping(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5,decimal_places=2)

class Order(models.Model):
    crust = models.ForeignKey(Crust,on_delete=models.CASCADE)

class OrderTopping(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    topping = models.ForeignKey(Topping,on_delete=models.CASCADE)
