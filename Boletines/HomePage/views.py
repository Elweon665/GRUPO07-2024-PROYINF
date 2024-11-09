from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.http import FileResponse, Http404, JsonResponse
from .models import PDF
from .forms import TagSelectionForm
import os
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomAuthenticationForm
from django.contrib import messages
from .forms import UserRegistrationForm

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


def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "El usuario no existe o las credenciales son incorrectas.")  # Agregar mensaje de error
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Crea el usuario
            messages.success(request, "Tu cuenta ha sido creada exitosamente. Ahora puedes iniciar sesión.")
            return redirect('login')  # Redirige a la página de inicio de sesión
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
