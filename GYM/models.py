from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.


class GYM(models.Model):
    name = models.CharField(max_length=255)
    number_of_classes = models.IntegerField()
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Classes(models.Model):
    gym = models.ForeignKey(GYM, on_delete=models.CASCADE)
    type_of = models.ForeignKey(Type, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    limits = models.IntegerField()
    description = models.TextField()
    start = models.DateTimeField(default=now)
    end = models.DateTimeField(default=now)
    price = models.DecimalField(decimal_places=2, max_digits=2)
    img = models.ImageField(blank=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    class_of = models.ForeignKey(Classes, on_delete=models.CASCADE)
    time = models.DateTimeField(default=now)

    def __str__(self):
        return self.class_of.name
