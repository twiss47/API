from django.db import models

# Create your models here.


#================== CAR ==================


class Car(models.Model):
    brand = models.CharField(max_length=155)
    name = models.CharField(max_length=155)
    year = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.name} {self.brand}'
    
    