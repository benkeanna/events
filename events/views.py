from django.shortcuts import render
from django.http import HttpResponse


def index(request):

    return HttpResponse(request, 'events/index.html')


def event_listing(request):
    html = '''
    <ul>
        <li>Chill on the beach <a href="chill">chill</a></li>
        <li>Camping in the woods <a href="camp">camp</a></li>
        <li>Flying into space <a href="fly">fly</a></li>
    </ul>
    '''
    return HttpResponse(html)


def event_detail(request, name):
    data = {
        'chill': '<h2>Chill on the beach just for 500 dolars.</h2>',
        'camp':  '<h2>Camp in the woods for 1000 dolars.</h2>',
        'fly': '<h2>Fly high for free.</h2>'
    }

    select = data.get(name)

    if select:
        return HttpResponse(select)
    else:
        return HttpResponse('No such thing')
