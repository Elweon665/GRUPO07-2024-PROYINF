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
    '''
    interests = scrap_urls()
    return render(request, 'scrap_view.html', {'interests': interests})
    '''
    # interests = scrap_urls()
    # interests = scrap_apnews()
    # interests = scrap_aedyr()
    interests = scrap_agricology()

    return render(request, 'scrap_view.html', {'interests': interests})


def show_content(request):
    #interest = scrap_urls()
    #interest = scrap_apnews()
    #interest = scrap_aedyr()
    interest = scrap_agricology()
    interests = [scrap_agricology_article(inter['link']) for inter in interest]
    values = []
    for i in range(0,len(interest)):
        values.append({'title': interest[i]['title'],'content': interests[i]['content']})

    return render(request, 'news_view.html', {'interest': values})

def update_db(request):
    if request.method == "POST":
        database_update()  # Llama a la función que deseas ejecutar
        return JsonResponse({"success": True, "message": "Base de datos actualizada correctamente"})
    return JsonResponse({"success": False, "message": "Método no permitido"}, status=405)

