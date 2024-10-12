from django.http import HttpResponse
from django.template import loader
from django.http import FileResponse
import os

def test(request):
    template = loader.get_template('primerHTML.html')
    return HttpResponse(template.render())

def descargar_boletin(request):
    file_path =  r'C:\Users\holis\OneDrive\Escritorio\Analisis y diseño\GRUPO07-2024-PROYINF-main\Boletines\HomePage\templates\PDFs\articles-126720_archivo_01.pdf'
    response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="mi_boletin.pdf" '
    return response