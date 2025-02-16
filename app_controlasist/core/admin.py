from django.contrib import admin
from .models import Empleados, Asistencia

# Register your models here.
admin.site.register([Empleados,Asistencia])