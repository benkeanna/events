from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Event, EventRun
from .forms import EventForm, EventRunForm, EventFilterForm


def index(request):
	"""Home page.
	"""
	return render(request, 'events/index.html')


def event_listing(request, category=None):
	"""Page with all events.
	"""
	events = Event.objects.filter_by_category(category)

	if request.GET:
		filter_form = EventFilterForm(request.GET)
		if filter_form.is_valid():
			events = Event.objects.filter_available(**filter_form.cleaned_data)
	else:
		filter_form = EventFilterForm()

	paginator = Paginator(events, 1)
	page = request.GET.get('page')
	events = paginator.get_page(page)

	return render(request, 'events/event_listing.html',
	              {'events': events, 'filter_form': filter_form})


def event_detail(request, pk):
	"""Page with event detail.
	"""
	event = Event.objects.get(pk=pk)
	runs = event.eventrun_set.all().order_by('date')
	args = {'event': event, 'runs': runs}

	return render(request, 'events/event_detail.html', args)


@login_required
def my_events(request):
	"""Page with events created by user.
	"""
	events = Event.objects.all().filter(host_id=request.user.id)

	return render(request, 'events/my_events.html', {'events': events})


@login_required
def create_event(request):
	"""Event creation page.
	"""
	if request.method == 'POST':
		form = EventForm(request.POST)

		if form.is_valid():
			event = form.save(commit=False)
			event.host = request.user
			event.save()

			return redirect('my_events')

	args = {'form': EventForm}
	return render(request, 'events/create_event.html', args)


@login_required
def update_event(request, pk):
	"""Event updating page.
	"""
	event = Event.objects.get(pk=pk)
	
	if request.method == 'POST':
		form = EventForm(request.POST, instance=event)

		if form.is_valid():
			event = form.save(commit=False)
			event.host = request.user
			event.save()

			return redirect('my_events')

	args = {'form': EventForm(instance=event)}
	return render(request, 'events/update_event.html', args)


@login_required
def delete_event(request, pk):
	"""Deletes event..
	"""
	Event.objects.get(pk=pk).delete()

	return redirect('my_events')


@login_required
def create_event_run(request, event_id):
	"""Event run creation page.
	"""
	if request.method == 'POST':
		form = EventRunForm(request.POST)
		
		if form.is_valid():
			event_run = form.save(commit=False)
			event_run.event = Event.objects.get(pk=event_id)
			event_run.save()
			
		return redirect('/events/detail/{}/'.format(event_id))
	
	args = {'form': EventRunForm}
	return render(request, 'events/create_event_run.html', args)


@login_required
def update_event_run(request, event_run_id):
	"""Event run updating page.
	"""
	event_run = EventRun.objects.get(pk=event_run_id)
	
	if request.method == 'POST':
		form = EventRunForm(request.POST, instance=event_run)
		
		if form.is_valid():
			event_run = form.save()
			event_id = event_run.event.id
			url = '/events/detail/{}'.format(event_id)
			return redirect(url)
	
	args = {'form': EventRunForm(instance=event_run)}
	return render(request, 'events/update_event_run.html', args)


@login_required
def delete_event_run(request, event_run_id):
	"""Deletes event run.
	"""
	run = EventRun.objects.get(pk=event_run_id)
	event_id = run.event.id
	run.delete()
	
	url = '/events/detail/{}'.format(event_id)
	return redirect(url)
