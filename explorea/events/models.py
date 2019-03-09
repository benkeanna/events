from django.db import models
from django.utils import timezone
from django.db.models import Max
from django.conf.global_settings import AUTH_USER_MODEL


class EventQuerySet(models.QuerySet):

	def filter_by_category(self, category=None):
		db_equivalent = ''
		for pair in self.model.CATEGORY_CHOICES:
			if pair[1] == category:
				db_equivalent = pair[0]
				break
		else:
			return self.all()

		return self.filter(category=db_equivalent)

	def filter_available(self, date_from=None, date_to=None, guests=None):
		# filter first all the eventruns and then get the ids to events
		date_from = date_from or timezone.now().date()

		if date_to:
			qs = EventRun.objects.filter(date__range=(date_from, date_to))
		else:
			qs = EventRun.objects.filter(date__gte=date_from)

		if guests:
			qs = qs.filter(seats_available__gte=guests)

		return self.filter(pk__in=[qs.values_list('event', flat=True)])


class EventManager(models.Manager):

	def get_queryset(self):
		return EventQuerySet(self.model, using=self._db)


class Event(models.Model):
	"""
	Basic event model.
	"""
	TRAVEL = 'TV'
	RELAX = 'RX'
	MUSIC = 'MC'
	EDUCATION = 'EC'

	CATEGORY_CHOICES = (
		(TRAVEL, 'travel'),
		(RELAX, 'relax'),
		(MUSIC, 'music'),
		(EDUCATION, 'education'),
	)

	host = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)

	name = models.CharField(max_length=200)
	description = models.TextField(max_length=1000)
	location = models.CharField(max_length=500)
	category = models.CharField(
			max_length=20,
			choices=CATEGORY_CHOICES,
			default=RELAX,
	)

	objects = EventManager()

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['name']


class EventRun(models.Model):
	"""
	Basic model for one event run.
	"""
	event = models.ForeignKey(Event, on_delete=models.CASCADE)

	date = models.DateField(blank=False, null=False)
	time = models.TimeField(blank=False, null=False)
	seats_available = models.PositiveIntegerField(blank=False, null=False)
	price = models.DecimalField(
			max_digits=10, decimal_places=2, blank=False, null=False)
