from django.shortcuts import render
from .models import Empleados, Asistencia
from django.http import HttpResponse, JsonResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import mm
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor
from io import BytesIO
from django.utils.timezone import now
import requests


# Create your views here.
def listar_empleados(request):
    empleados= Empleados.objects.all() #Select * from empleados
    return render(request, 'lista.html', {'empleados': empleados})

LOGO_URL= "https://www.salesianostalca.cl/images/2018/06/09/insignia.png"

SELLO_URL= "https://www.salesianostalca.cl/images/2018/06/09/insignia.png"

def generar_carnets(request):
    empleados= Empleados.objects.all()
    
    response= HttpResponse(content_type= 'application/pdf')
    response['Content-Disposition']= 'attachment; filename="carnets_empleados.pdf"'
    
    pdf= canvas.Canvas(response,pagesize=(53.98 * mm, 85.6 * mm)) #Tamaño ID-1 en vertical
    
    #Funcion para obtener imagenes de URL
    def obtener_imagenes(url):
        try:
            response= requests.get(url, stream=True)
            if response.status_code== 200:
                return ImageReader(BytesIO(response.content))
        except:
            return None
        return None

    logo_image= obtener_imagenes(LOGO_URL)
    sello_image= obtener_imagenes(SELLO_URL)
    
    for empleado in empleados:
        #Fondo degradado o con textura moderna
        pdf.setFillColor(HexColor("#1E3A8A"))
        pdf.rect(0, 0, 53.98 * mm, 85.6 * mm, fill= True, stroke= False)
        #Borde con efecto de sombre
        pdf.setFillColor(HexColor("#2563EB"))
        pdf.rect(3 * mm, 3 * mm, 47.98 * mm, 79.6 * mm, fill= True, stroke= False)
        #Insertar sello de agua 
        if sello_image: 
            pdf.setFillAlpha(0.1)
            pdf.drawImage(sello_image, 7 * mm, 35 * mm, width= 40 * mm, height= 40 * mm, mask= 'auto')
            pdf.setFillAlpha(1)
        
        #Insertar logo en la parte superior derecha 
        if logo_image:
            pdf.drawImage(logo_image, 38 * mm, 73 * mm, width= 9 * mm, height= 8 * mm, mask= 'auto')
            
        #Texto del carnet por mejor jerarquia o mejor nivel
        #nombre empresa
        pdf.setFillColorRGB(1, 1, 1)
        pdf.setFont("Times-Bold", 11)
        pdf.drawCentredString(26.99 * mm, 75 * mm, "Nombre_Empresa")
        
        pdf.setFont("Helvetica-Bold", 9)
        pdf.drawCentredString(26.99 * mm, 69 * mm, f"{empleado.nombre}")
        pdf.drawCentredString(26.99 * mm, 65 * mm, f"{empleado.codigo}")
        
        #linea divisora
        pdf.setStrokeColor(HexColor("#FFFFFF"))
        pdf.line(5 * mm, 62 * mm, 49 * mm, 62 * mm)
        
        if empleado.foto: 
            foto_path= empleado.foto.path
            pdf.drawImage(ImageReader(foto_path), 10 * mm, 23 * mm, width= 34 * mm, height= 34 * mm, mask= "auto")
        
        if empleado.codigo_barras:
            codigo_barras_path = empleado.codigo_barras.path
            pdf.drawImage(ImageReader(codigo_barras_path), 10 * mm, 5 * mm, width= 34 * mm, height= 15 * mm, mask= 'auto')
            
        pdf.showPage()
    pdf.save()
    return response

def registrar_asistencia(request):
    if request.method == "POST":
        codigo_barras= request.POST.get("codigo_barras", "").strip()
        
        try: 
            empleado= Empleados.objects.get(codigo = codigo_barras)
            Asistencia.objects.create(empleado= empleado, fecha_hora= now())
            
            foto_url= empleado.foto.url if empleado.foto else "/static/img/default.jpg"
            
            return JsonResponse({
                "success": True,
                "message":f"Asistencia registrada para: {empleado.nombre}",
                "nombre": empleado.nombre,
                "foto": foto_url,
            }) 
            
        except Empleados.DoesNotExist:
            return JsonResponse({
                "success": False, 
                "message": "Colaborador no encontrado"
            })
        
    return render(request, "asistencia.html")

def dashboard(request):
    return render(request, 'dashboard.html')