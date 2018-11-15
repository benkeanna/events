from django.shortcuts import render
from django.http import HttpResponse

from .models import Event, EventRun


def index(request):
    """
    Basic view of main page.
    """

    return render(request, 'events/index.html')


def event_listing(request):
    """
    Page with all events.
    """
    events = Event.objects.all()

    return render(request, 'events/event_listing.html', {'events': events})


def eventrun_listing(request):
    """
    page with all event runs.
    """
    eventruns = EventRun.objects.all()

    return render(request, 'events/eventrun_listing.html',
                  {'eventruns': eventruns})


def event_detail(request, name):
    """
    Page with event detail.
    """
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
