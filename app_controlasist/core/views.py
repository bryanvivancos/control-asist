from django.shortcuts import render
from .models import Empleados, Asistencia

# Create your views here.
def listar_empleados(request):
    empleados= Empleados.objects.all() #Select * from empleados
    return render(request, 'lista.html', {'empleados': empleados})
