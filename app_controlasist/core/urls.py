from django.urls import path
from .views import listar_empleados, generar_carnets, registrar_asistencia, dashboard

urlpatterns = [
    path('listar_empleados',listar_empleados, name="listar_empleados"),
    path('carnets', generar_carnets, name="generar_carnets"),
    path('asistencia', registrar_asistencia, name="registrar_asistencia"),
    path('', dashboard, name="dashboard"),
]
