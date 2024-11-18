from django.shortcuts import render
from .services.scraping import scrap_urls
from .services.scraping import scrap_news
from .services.scraping import scrap_apnews
from .services.scraping import scrap_apnews_article
from .services.scraping import scrap_aedyr
from .services.scraping import scrap_aedyr_article

def show_scrap(request):
    '''
    interests = scrap_urls()
    return render(request, 'scrap_view.html', {'interests': interests})
    '''
    # interests = scrap_urls()
    # interests = scrap_apnews()
    interests = scrap_aedyr()

    return render(request, 'scrap_view.html', {'interests': interests})


def show_content(request):
    #interest = scrap_urls()
    #interest = scrap_apnews()
    interest = scrap_aedyr()
    interests = [scrap_aedyr_article(inter['link']) for inter in interest]
    values = []
    for i in range(0,len(interest)):
        values.append({'title': interest[i]['title'],'content': interests[i]['content']})

    return render(request, 'news_view.html', {'interest': values})

