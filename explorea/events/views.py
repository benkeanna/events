from django.shortcuts import render, redirect

from .models import Event
from .forms import EventForm


def index(request):
    return render(request, 'events/index.html')


def event_listing(request):
    events = Event.objects.all()

    return render(request, 'events/event_listing.html', {'events': events})


def event_detail(request, pk):
    event = Event.objects.get(pk=pk)
    runs = event.eventrun_set.all().order_by('happens')
    args = {'event': event, 'runs': runs}

    return render(request, 'events/event_detail.html', args)


def my_events(request):
    events = Event.objects.all().filter(host_id=request.user.id)

    return render(request, 'events/my_events.html', {'events': events})


def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)

        if form.is_valid():
            event = form.save(commit=False)
            event.host = request.user
            event.save()

            return redirect('my_events')

    form = EventForm
    return render(request, 'events/create_event.html', {'form': form})


def delete_event(request, pk):
    Event.objects.get(pk=pk).delete()

    return redirect('my_events')


def update_event(request, pk):
	event = Event.objects.get(pk=pk)

	if request.method == 'POST':
		form = EventForm(request.POST, instance=event)

		if form.is_valid():
			event = form.save(commit=False)
			event.host = request.user
			event.save()

			return redirect('my_events')

	form = EventForm(instance=event)
	return render(request, 'events/update_event.html', {'form': form})
