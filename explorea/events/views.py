from django.shortcuts import render, redirect

from .models import Event
from .forms import CreateEventForm


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


def my_events(request):
    """
    Page with all users events.
    """
    events = Event.objects.all().filter(host_id=request.user.id)

    return render(request, 'events/my_events.html', {'events': events})


def create_event(request):
    """
    Form for event creation.
    """
    if request.method == 'POST':
        form = CreateEventForm(request.POST)

        if form.is_valid():
            host_id = form.cleaned_data.get('host_id')

            form.save()

            return redirect('my_events')

    form = CreateEventForm
    return render(request, 'events/create_event.html', {'form': form})
