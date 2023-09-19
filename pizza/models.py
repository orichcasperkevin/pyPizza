from django.db import models

# Create your models here.
class Crust(models.Model):
    SIZES = [
        (1,'SMALL'),
        (2,'MEDIUM'),
        (3,'LARGE'),
        (4,'XLARGE')
    ]
    size = models.IntegerField(choices=SIZES)
    price = models.DecimalField(max_digits=7,decimal_places=2)

    def __str__(self):
        return f"{self.size}-@-{self.price}"

    class Meta:
        unique_together = [['size','price']]

class Topping(models.Model):
    name = models.CharField(max_length=100,unique=True)
    price = models.DecimalField(max_digits=5,decimal_places=2)

    def __str__(self):
        return self.name

class Order(models.Model):
    phonenumber = models.CharField(max_length=20)
    crust = models.ForeignKey(Crust,on_delete=models.CASCADE)
    topping = models.ForeignKey(Topping,on_delete=models.CASCADE)
