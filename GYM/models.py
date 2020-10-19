from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.mail import send_mail
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.template.loader import render_to_string

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
    price = models.DecimalField(decimal_places=2, max_digits=4)
    img = models.ImageField(blank=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    class_of = models.ForeignKey(Classes, on_delete=models.CASCADE)
    time = models.DateTimeField(default=now)

    def __str__(self):
        return self.class_of.name


@receiver(post_save, sender=Booking)
def get_email(instance, *args, **kwargs):
    email = instance.customer.email
    sub = 'Class Booking information'
    msg = render_to_string('email.html', {'name': instance.customer.username, 'class': instance.class_of.name,
                                          'start': instance.class_of.start, 'end': instance.class_of.end, 'id': instance.id})
    #msg = f'Congratulations " {instance.customer.username} " for being a member of " {instance.class_of.name} " class.\nIt will start: {instance.class_of.start}.\nEnd: {instance.class_of.end}.\nYour booking id: {instance.id}\n\n Thank You'
    send_mail(sub, msg, settings.EMAIL_HOST_USER,
              [email, ], fail_silently=False)
