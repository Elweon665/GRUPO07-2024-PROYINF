from django.urls import path
from . import views


"""
Para hacer la llamada de la app a una direción url en particular de la página,
se deben crear los urlpatterns de la siguiente forma:

path('Nombre_URL/', nombre_archivo.nombre_funcion, name=etiqueta_referenciación)

La parte Nombre_URL/ sirve para indicar que se debe llamar a esa APP solamente 
cuando el usuario entre a la página nombrePagina.com/Nombre_URL
"""
urlpatterns = [
    path('', views.test, name='HomePage'),
    path('descargar-boletin/', views.descargar_boletin, name='descargar_boletin'),
]