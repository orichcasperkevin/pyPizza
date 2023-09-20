from django.db import models

# Create your models here.
SIZES = [
    (1,'small'),
    (2,'medium'),
    (3,'large'),
    (4,'extra large')
]

class Crust(models.Model):
    size = models.IntegerField(choices=SIZES)
    price = models.DecimalField(max_digits=7,decimal_places=2)

    def __str__(self):
        return f"{self.size} @ {self.price}"

    @property
    def display_name(self):
        return SIZES[self.size -1][1]

    class Meta:
        unique_together = [['size','price']]

class Topping(models.Model):
    name = models.CharField(max_length=100,unique=True)
    price = models.DecimalField(max_digits=5,decimal_places=2)

    def __str__(self):
        return self.name


class Order(models.Model):
    phone_number = models.CharField(max_length=20)
    crust = models.ForeignKey(Crust,on_delete=models.CASCADE)
    topping = models.ForeignKey(Topping,on_delete=models.CASCADE,null=True)
    draft = models.BooleanField(default=True)


class OrderMessageConfig(models.Model):
    welcome_message = models.TextField(max_length=100)

    def save(self,*args,**kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(OrderMessageConfig, self).save(*args, **kwargs)
