from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from scraping.models import Scrap

def get_content_AJAX(url):
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "es-ES,es;q=0.9,en-US;q=0.8,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html_content = session.get(f'{url}').text
    
    return html_content

def get_content(url):
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "es-ES,es;q=0.9,en-US;q=0.8,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html_content = session.get(f'{url}').text
    
    return html_content

'''
Esta función se encarga de recolectar todo el contenido oculto que requiera de solicitudes AJAX.
''' 
def scrap_urls():
    interests = []
    offset = 0
    link = (
        "https://www.1pointfive.com/index.php?"
        "p=actions/sprig-core/components/render&query=&"
        f"offset={offset}&" 
        "sprig%3AsiteId=89a002b92bd369e8b94cf1f4758bb51a5345fe07e61d4d640f922c84585e39341&"
        "sprig%3Aid=44b9d50228ee1a9c35b2f43bdf23671ae58c46b905888c206cd245a943bd6293component-glzwiy&"
        "sprig%3Acomponent=72c279dec967a4f057ab02c2bcc6c4b67d8da616dc7f1af36b0e50ae557db421&"
        "sprig%3Atemplate=372a460adcbd047b6b2d1c236a6a869f2b3d576dfb1d2570dc1874d12cbcf47cblocks%2Fpartials%2Fnews%2F_listing&"
        "sprig%3Avariables%5BsectionQuery%5D=a1542e8471298b71f36ff6e27f6963e44d86091817dc7533594563c712dc1f47news&"
        "sprig%3Avariables%5B_limit%5D=c22e006248cea17959818d9dae437daa99fe6197c3035fda330ae3c0206effea8&"
        "sprig%3Avariables%5Boffset%5D=fdc6eb6dbdcbc08c660b7748a0833dd75d9a73d1874d91d17825fffd7aee9d790"
    )
    
    # Aquí se va a obtener el contenido de la noticia más nueva que posee una clase HTML distinta al resto
    html_content = get_content_AJAX(link)
    soup = BeautifulSoup(html_content, 'html.parser')
    articles = soup.find_all('article', class_='group flex flex-col lg:col-span-2 lg:row-span-2 bg-cloud')
    for article in articles:
        title_div = article.find('div', class_='max-w-xl flex flex-col justify-between p-8 lg:p-16 lg:max-w-none')
        title = title_div.find('h3').text.strip()
        link = title_div.find('h3').find('a')['href']
        interests.append({'title': title, 'link': link})
    
    # Aquí se hacen las dinstintas llamadas AJAX para obtener todas las demás noticias de la página
    while True:
        link = (
            "https://www.1pointfive.com/index.php?"
            "p=actions/sprig-core/components/render&query=&"
            f"offset={offset}&" 
            "sprig%3AsiteId=89a002b92bd369e8b94cf1f4758bb51a5345fe07e61d4d640f922c84585e39341&"
            "sprig%3Aid=44b9d50228ee1a9c35b2f43bdf23671ae58c46b905888c206cd245a943bd6293component-glzwiy&"
            "sprig%3Acomponent=72c279dec967a4f057ab02c2bcc6c4b67d8da616dc7f1af36b0e50ae557db421&"
            "sprig%3Atemplate=372a460adcbd047b6b2d1c236a6a869f2b3d576dfb1d2570dc1874d12cbcf47cblocks%2Fpartials%2Fnews%2F_listing&"
            "sprig%3Avariables%5BsectionQuery%5D=a1542e8471298b71f36ff6e27f6963e44d86091817dc7533594563c712dc1f47news&"
            "sprig%3Avariables%5B_limit%5D=c22e006248cea17959818d9dae437daa99fe6197c3035fda330ae3c0206effea8&"
            "sprig%3Avariables%5Boffset%5D=fdc6eb6dbdcbc08c660b7748a0833dd75d9a73d1874d91d17825fffd7aee9d790"
        )
        html_content = get_content_AJAX(link)
        soup = BeautifulSoup(html_content, 'html.parser')
        articles = soup.find_all('article', class_='group flex flex-col card')

        if not articles:
            break  

        for article in articles:
            title_div = article.find('div', class_='max-w-xl flex flex-col justify-between mt-4')
            title = title_div.find('h3').text.strip()
            link = title_div.find('h3').find('a')['href']
            interests.append({'title': title, 'link': link})

        offset += 8  

    return interests

'''
Esta función se encarga de recolectar el contenido de todas las noticias scrapeadas de los sitios de noticias.
'''
def scrap_news(link):
    html_content = get_content(link)
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Fecha del artículo si es que aplica
    date = soup.find('time') 
    date_text = date.text.strip() if date else None

    # Cuerpo/Contenido de la noticia
    content_div = soup.find('article', class_='pb-10 px-4 prose max-w-[80ch] prose-slate mx-auto md:prose-lg lg:px-0 prose-hr:mb-5')
    paragraphs = content_div.find_all('p') if content_div else []
    article_text = "\n".join([p.text.strip() for p in paragraphs])

    return {
        "date": date_text,
        "content": article_text
    }
    

def scrap_apnews():
    interests = []
    
    for offset in range(1,7):
        url = ("https://apnews.com/hub/water-quality?"
            f"p={offset}")
        html_content = get_content_AJAX(url)
        soup = BeautifulSoup(html_content, 'html.parser')
        articles = soup.find_all('div', class_='PageList-items-item')
        
        for article in articles:
            title = article.find('h3').text.strip()
            link = article.find('h3').find('a')['href']
            interests.append({'title': title, 'link': link})
    
    return interests
    

def scrap_apnews_article(link):
    html_content = get_content(link)
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Fecha del artículo si es que aplica
    date = soup.find('time')
    date_text = date.text.strip() if date else None
    
    # Cuerpo/Contenido de la noticia
    content_div = soup.find('div', class_='RichTextStoryBody RichTextBody')
    paragraphs = content_div.find_all('p') if content_div else []
    article_text = "\n".join([p.text.strip() for p in paragraphs])

    return {
        "date": date_text,
        "content": article_text
    }
    

# A esta funcion le faltan articulos
def scrap_aedyr():
    interests = []
    
    for offset in range(1,7):
        url = ("https://aedyr.com/eventos/")
        html_content = get_content_AJAX(url)
        soup = BeautifulSoup(html_content, 'html.parser')
        articles = soup.find_all('div', class_='jornad-cols')
        
        for article in articles:
            link = article.find('a')['href']
            title = article.find('a').find('h2').text.strip()
            if not any(item['title'] == title for item in interests):
                interests.append({'title': title, 'link': link})
                
        articles = soup.find_all('div', class_='eventos-digitales-cols')
        
        for article in articles:
            link = article.find('a')['href']
            title = article.find('a').find('h2').text.strip()
            if not any(item['title'] == title for item in interests):
                interests.append({'title': title, 'link': link})
    
    return interests

def scrap_aedyr_article(link):
    html_content = get_content(link)
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Fecha del artículo si es que aplica
    date = soup.find('time')
    date_text = date.text.strip() if date else None
    
    # Cuerpo/Contenido de la noticia
    content_div = soup.find('div', class_='et_pb_text_inner')
    if content_div:
        # Busca el título en el h3, si existe
        title_element = content_div.find('h3')
        title = title_element.text.strip() + "\n" if title_element else ""
        
        # Busca todos los párrafos dentro del div
        paragraphs = content_div.find_all('p')
        article_text = title + "\n".join([p.text.strip() for p in paragraphs])
    else:
        # Si no se encuentra el div
        article_text = "Contenido no encontrado"

    return {
        "date": date_text,
        "content": article_text
    }
    
'''
Las funciones de la página https://www.aguasresiduales.info/revista/noticias las dejaré para el final, son demasiadas noticias
y si las llamo todas de una nuestra página y la de ellos se caen.
def scrap_ares():
    return

def scrap_ares_article():
    return
'''


def scrap_agricology():
    interests = []
    offset = 1
    found = True
    while found:
        found = False
        url = ("https://agricology.co.uk/events/?_"
                f"paged={offset}")
        html_content = get_content_AJAX(url)
        soup = BeautifulSoup(html_content, 'html.parser')
        articles = soup.find('div', class_='fwpl-layout events-post-block')
        if articles == '<div class="fwpl-layout events-post-block"></div>':
            break
        
        i = 1
        while True:
            article = articles.find('div', class_='fwpl-result r' + str(i))
            if article == None:
                break
            title = article.find('div', class_='fwpl-item farmer-grid-title').find('h3').text.strip()
            link = article.find('div', class_='fwpl-item farmer-grid-thumb').find('a')['href']
            interests.append({'title': title, 'link': link})
            found = True
            i += 1
        
        offset += 1
    
    return interests

def scrap_agricology_article(link):
    html_content = get_content(link)
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Cuerpo/Contenido de la noticia
    content_div = soup.find('div', class_='entry-content')
    if content_div:
        # Busca el título en el h3,
        
        title = content_div.find('div', class_='col-md-12')
        title = title.find('h1').text.strip()
        # title = title.find('h1').text.strip()
        date = content_div.find('div', class_='event-meta').text.strip()[7:]
        
        content = content_div.find('div', class_='row d-flex justify-content-between')
        text = content.find_all('p')
        # Junta todos los parrafos encontrados en el div
        article_text = title + "\n".join([p.text.strip() for p in text])
    else:
        # Si no se encuentra el div
        article_text = "Contenido no encontrado"
        

    return {
        "date": date,
        "content": article_text
    }
    
def database_update():
    interest = scrap_urls()
    titulo = [p['title'] for p in interest]
    link = [p['link'] for p in interest]
    interests = [scrap_news(p['link']) for p in interest]
    interest = [p['content'] for p in interests]
    final = zip(titulo, link, interests)
    scrap_objects = [Scrap(title=title, link=link, content=content) for title, link, content in final]
    Scrap.objects.bulk_create(scrap_objects, ignore_conflicts=True)
    
    interest = scrap_apnews()
    titulo = [p['title'] for p in interest]
    link = [p['link'] for p in interest]
    interests = [scrap_apnews_article(p['link']) for p in interest]
    interest = [p['content'] for p in interests]
    final = zip(titulo, link, interests)
    scrap_objects = [Scrap(title=title, link=link, content=content) for title, link, content in final]
    Scrap.objects.bulk_create(scrap_objects, ignore_conflicts=True)
    
    interest = scrap_aedyr()
    titulo = [p['title'] for p in interest]
    link = [p['link'] for p in interest]
    interests = [scrap_aedyr_article(p['link']) for p in interest]
    interest = [p['content'] for p in interests]
    final = zip(titulo, link, interests)
    scrap_objects = [Scrap(title=title, link=link, content=content) for title, link, content in final]
    Scrap.objects.bulk_create(scrap_objects, ignore_conflicts=True)
    
    interest = scrap_agricology()
    titulo = [p['title'] for p in interest]
    link = [p['link'] for p in interest]
    interests = [scrap_agricology_article(p['link']) for p in interest]
    interest = [p['content'] for p in interests]
    final = zip(titulo, link, interests)
    scrap_objects = [Scrap(title=title, link=link, content=content) for title, link, content in final]
    Scrap.objects.bulk_create(scrap_objects, ignore_conflicts=True)
    
    
    return