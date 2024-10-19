from django.shortcuts import render
from .services.scraping import scrap_urls
from .services.scraping import scrap_news

def show_scrap(request):
    '''
    interests = scrap_urls()
    return render(request, 'scrap_view.html', {'interests': interests})
    '''
    interests = scrap_urls()

    return render(request, 'scrap_view.html', {'interests': interests})


def show_content(request):
    interest = scrap_urls()
    interests = [scrap_news(inter['link']) for inter in interest]
    values = []
    for i in range(0,len(interest)):
        values.append({'title': interest[i]['title'],'content': interests[i]['content']})

    return render(request, 'news_view.html', {'interest': values})

