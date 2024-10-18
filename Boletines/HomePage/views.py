from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.http import FileResponse, Http404, JsonResponse
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
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = TagSelectionForm()

    return render(request, 'generar.html', {'form': form, 'success_message': success_message})