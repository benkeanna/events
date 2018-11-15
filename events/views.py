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


def event_detail(request, pk):
    """
    Page with event detail.
    """
    event = Event.objects.get(pk=pk)
    runs = event.eventrun_set.all().order_by('happens')
    args = {'event': event, 'runs': runs}

    return render(request, 'events/event_detail.html', args)
