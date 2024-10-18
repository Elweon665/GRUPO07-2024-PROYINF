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
#    path('', views.test, name='HomePage'),
    path('', views.lista_boletines, name='lista_boletines'),
    path('view/<int:pdf_id>/', views.view_pdf, name='view_pdf'),
    path('download/<int:pdf_id>/', views.download_pdf, name='download_pdf'),
    path('tags/', views.generar, name='generar'),
]