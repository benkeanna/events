from django import forms
from django.utils import timezone

from .models import Event, EventRun


class EventForm(forms.ModelForm):

	class Meta:
		model = Event
		fields = [
			'name',
			'description',
			'location',
			'category',
		]

	class Meta:
		model = Event
		exclude = ['host', 'slug']


class EventRunForm(forms.ModelForm):
	date = forms.DateField(input_formats=["%d.%m.%Y"],
	                       widget=forms.DateInput(format='%d.%m.%Y'))
	
	class Meta:
		model = EventRun
		exclude = ['event']


class EventFilterForm(forms.Form):
	PRICE_ASC = 'price'
	PRICE_DESC = '-price'
	SEATS = '-seats_available'
	DATE = 'date'
	NAME = 'event__name'
	HOST = 'event__host__username'

	SORT_CHOICES = (
		(PRICE_ASC, 'cheapest'),
		(PRICE_DESC, 'most expensive'),
		(SEATS, 'seats available'),
		(DATE, 'date'),
		(NAME, 'name'),
		(HOST, 'host'),
	)

	date_from = forms.DateField(label='From', initial=None,
	                            widget=forms.SelectDateWidget, required=False)

	date_to = forms.DateField(label='To', initial=None,
	                          widget=forms.SelectDateWidget, required=False)

	guests = forms.IntegerField(required=False, min_value=1)

	sort_by = forms.ChoiceField(label="Sort by", choices=SORT_CHOICES,
	                            required=False)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.initial['sort_by'] = 'date'

	def clean(self):
		super().clean()
		date_from = self.cleaned_data.get('date_from')
		date_to = self.cleaned_data.get('date_to')

		if ((date_from and date_to) and
				date_from > date_to):
			self.add_error('date_from', 'Date selected later than date To')

		for name, date in [('date_from', date_from),
		                   ('date_to', date_to)]:
			if date and date < timezone.now().date():
				self.add_error(name, 'Selected date in the past')

		if not self.cleaned_data.get('sort_by'):
			self.cleaned_data['sort_by'] = 'date'
		self.cleaned_data
