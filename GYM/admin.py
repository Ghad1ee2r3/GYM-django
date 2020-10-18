from django.contrib import admin
from .models import GYM, Type, Classes, Booking

# Register your models here.

admin.site.register(GYM)
admin.site.register(Type)
admin.site.register(Classes)
admin.site.register(Booking)
