from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    html = '''
    Hey, app running.
    Check <a href="/events">offer</a>
    '''
    return HttpResponse(html)


def event_listing(request):
    html = '''
    <ul>
        <li>Chill on the beach</li>
        <li>Camping in the woods</li>
        <li>Flying into space</li>
    </ul>
    '''
    return HttpResponse(html)
