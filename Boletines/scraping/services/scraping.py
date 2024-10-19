from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

def get_content_AJAX(offset):
    url = (
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
    
def scrap_urls():
    interests = []
    offset = 0
    
    # Aquí se va a obtener el contenido de la noticia más nueva que posee una clase HTML distinta al resto
    html_content = get_content_AJAX(offset)
    soup = BeautifulSoup(html_content, 'html.parser')
    articles = soup.find_all('article', class_='group flex flex-col lg:col-span-2 lg:row-span-2 bg-cloud')
    for article in articles:
        title_div = article.find('div', class_='max-w-xl flex flex-col justify-between p-8 lg:p-16 lg:max-w-none')
        title = title_div.find('h3').text.strip()
        link = title_div.find('h3').find('a')['href']
        interests.append({'title': title, 'link': link})
    
    # Aquí se hacen las dinstintas llamadas AJAX para obtener todas las demás noticias de la página
    while True:
        html_content = get_content_AJAX(offset)
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
    