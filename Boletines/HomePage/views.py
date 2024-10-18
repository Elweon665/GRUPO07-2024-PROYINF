from django.http import HttpResponse
from django.template import loader
from django.http import FileResponse
import os

def test(request):
    template = loader.get_template('primerHTML.html')
    return HttpResponse(template.render())

def descargar_boletin(request):
    file_path =  r'Boletines\HomePage\templates\PDFs\articles-126720_archivo_01.pdf'
    response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="mi_boletin.pdf" '
    return response

def boletin_junio_2024_descargar(request):
    file_path =  r'Boletines\HomePage\templates\PDFs\articles-126033_archivo_01.pdf'
    response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Boletin_Junio_2024.pdf" '
    return response

def Consultarboletines(request):
    template = loader.get_template('Consultaboletines.html')
    return HttpResponse(template.render())

def mostrar_boletin(request):
    file_path = r'Boletines\HomePage\templates\PDFs\articles-126033_archivo_01.pdf'
    response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="mi_boletin.pdf"'
    return response

def Boletin_parametros(request):
    template = loader.get_template('Boletin_parametros.html')
    return HttpResponse(template.render())

def descargar_pdf(request):
    # Ruta completa del archivo PDF en el servidor
    pdf_path = os.path.join('Boletines/HomePage/templates/PDFs/', 'articles-126721_archivo_01.pdf')
    
    # Sirve el archivo PDF como una respuesta
    return FileResponse(open(pdf_path, 'rb'), content_type='application/pdf')

def enviar_parametros(request):
    file_path = r'Boletines\HomePage\templates\PDFs\articles-126721_archivo_01.pdf'
    response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="mi_boletin.pdf"'
    return response
def descargar_boletin(request):
    file_path =  r'Boletines\HomePage\templates\PDFs\articles-126720_archivo_01.pdf'
    response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="mi_boletin.pdf" '
    return response