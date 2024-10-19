from django.http import HttpResponse
from django.template import loader

def test(request):
    template = loader.get_template('primerHTML.html')
    return HttpResponse(template.render())
