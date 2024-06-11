from django.contrib import admin
from .models import Clase, Recibo, Reserva

# Register your models here.

admin.site.register(Clase)
admin.site.register(Recibo)
admin.site.register(Reserva)
