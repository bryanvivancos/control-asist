from django.db import models
from django.utils.crypto import get_random_string
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files.base import ContentFile


# Create your models here.
class Empleados(models.Model):
    nombre=models.CharField(max_length=100)
    codigo=models.CharField(max_length=100,unique=True)
    foto=models.ImageField(upload_to='fotos/',blank=True,null=True)
    codigo_barras=models.ImageField(upload_to='codigos/',blank=True,null=True)
    
    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo= get_random_string(10)
            
        """GENERANDO EL CODIGO DE BARRAS"""
        ean=barcode.get('code128',self.codigo,writer=ImageWriter())
        buffer=BytesIO()
        ean.write(buffer)
        self.codigo_barras.save(f"{self.codigo}.png", ContentFile(buffer.getvalue()), save=False)
        super().save(*args,**kwargs)

    def __str__(self):
        return self.nombre

class Asistencia(models.Model):
    empleado=models.ForeignKey(Empleados,on_delete=models.CASCADE)
    fecha_hora=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ingreso de {self.empleado.nombre} - {self.fecha_hora}"