from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.http import FileResponse, Http404
from .models import PDF
from .forms import TagSelectionForm
import os

def lista_boletines(request):
    pdfs = PDF.objects.all()
    return render(request, 'lista_boletines.html', {'pdfs': pdfs})

def view_pdf(request, pdf_id):
    try:
        pdf = PDF.objects.get(pk=pdf_id)
        return FileResponse(open(pdf.file.path, 'rb'), content_type='application/pdf')
    except PDF.DoesNotExist:
        raise Http404('PDF not found')
    
def download_pdf(request, pdf_id):
    try:
        pdf = PDF.objects.get(pk=pdf_id)
        response = FileResponse(open(pdf.file.path, 'rb'), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{pdf.file.name}"'
        return response
    except PDF.DoesNotExist:
        raise Http404('PDF not found')

def generar(request):
    success_message = None
    if request.method == 'POST':
        form = TagSelectionForm(request.POST)
        if form.is_valid():
            selected_tags = form.cleaned_data['tags']
            # Handle the selected tags
            success_message = "La IA(que no existe) NO esta generando el boletin deseado, prontamente el boletin NO estara disponible."
    else:
        form = TagSelectionForm()

    return render(request, 'generar.html', {'form': form, 'success_message': success_message})

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