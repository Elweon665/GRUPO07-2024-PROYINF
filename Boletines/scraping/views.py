from django.shortcuts import render
from django.http import JsonResponse
from .services.scraping import scrap_urls
from .services.scraping import scrap_news
from .services.scraping import scrap_apnews
from .services.scraping import scrap_apnews_article
from .services.scraping import scrap_aedyr
from .services.scraping import scrap_aedyr_article
from .services.scraping import scrap_agricology
from .services.scraping import scrap_agricology_article
from .services.scraping import database_update

def show_scrap(request):
    page = request.GET.get('page', 'default')  # Si no se envía "page", usa "default"

    # Decidir qué función de scraping ejecutar
    if page == "1pointfive":
        interests = scrap_urls() 
    elif page == "apnews":
        interests = scrap_apnews()  
    elif page == "aedyr":
        interests = scrap_aedyr()  
    elif page == "agricology":
        interests = scrap_agricology()  
    else:
        interests = []  

    return render(request, 'scrap_view.html', {'interests': interests})


def show_content(request):
    # Leer el parámetro 'page' del GET
    page = request.GET.get('page', '-')
    print(page)

    interest = []

    # Seleccionar la función de scraping según la página
    if page == "1pointfive":
        interest = scrap_urls()
        interests = [scrap_news(inter['link']) for inter in interest] if interest else []
    elif page == "aedyr":
        interest = scrap_aedyr()
        interests = [scrap_aedyr_article(inter['link']) for inter in interest] if interest else []
    elif page == "apnews":
        interest = scrap_apnews()
        interests = [scrap_apnews_article(inter['link']) for inter in interest] if interest else []
    elif page == "agricology":
        interest = scrap_agricology()
        interests = [scrap_agricology_article(inter['link']) for inter in interest] if interest else []

    values = [
        {'title': interest[i]['title'], 'content': interests[i]['content']}
        for i in range(len(interest))
    ]

    return render(request, 'news_view.html', {'interest': values, 'selected_page': page})


def update_db(request):
    if request.method == "POST":
        database_update() 
        return JsonResponse({"success": True, "message": "Base de datos actualizada correctamente"})
    return JsonResponse({"success": False, "message": "Método no permitido"}, status=405)

