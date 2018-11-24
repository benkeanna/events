from django.forms import ModelForm

from .models import Event, EventRun


class EventForm(ModelForm):

	class Meta:
		model = Event
		fields = [
			'name',
			'description',
			'location',
			'category',
		]


class EventRunForm(ModelForm):
	
	class Meta:
		model = EventRun
		fields = [
			'happens',
			'seats_available',
			'price',
		]
