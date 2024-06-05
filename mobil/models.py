from django.db import models

# Create your models here.
class Mobils(models.Model):
    
    TRANSMISSION = [
        ('Manual', 'Manual'),
        ('Automatic', 'Automatic'),
    ]
    
    TYPE_CAR = [
        ('Convertible','Convertible'),
        ('Coupe','Coupe'),
        ('Sedan','Sedan'),
        ('Hatchback','Hatchback'),
        ('SUV','SUV'),
        ('MPV','MPV'),
    ]

    name = models.CharField(max_length=100)
    stock = models.PositiveIntegerField()
    image1 = models.ImageField(upload_to="images/")
    image2 = models.ImageField(upload_to="images/")
    image3 = models.ImageField(upload_to="images/")
    pricePerDay = models.IntegerField()
    transmission = models.CharField(max_length=10, choices=TRANSMISSION)
    typeCar = models.CharField(max_length=20, choices=TYPE_CAR)
    description = models.CharField(max_length=150)
    seat = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}. {}".format(self.id, self.name)