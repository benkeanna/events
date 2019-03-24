from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.conf.global_settings import AUTH_USER_MODEL


def get_related_attr(obj, attrs):
    related_obj = obj
    for attr in attrs:
        related_obj = getattr(related_obj, attr)
    return related_obj


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


class EventRunQuerySet(models.QuerySet):

	def filter_by_category(self, category=None):
		db_equivalent = ''
		for pair in Event.CATEGORY_CHOICES:
			if pair[1] == category:
				db_equivalent = pair[0]
				break
		else:
			return self.all()

		return self.filter(event__category=db_equivalent)

	def filter_available(self, date_from=None, date_to=None, guests=None):
		# filter first all the eventruns and then get the ids to events
		date_from = date_from or timezone.now().date()

		if date_to:
			qs = self.filter(date__range=(date_from, date_to))
		else:
			qs = self.filter(date__gte=date_from)

		if guests:
			qs = qs.filter(seats_available__gte=guests)

		return qs

	def filter_first_available(self, date_from=None, date_to=None, guests=None, sort_by='date'):
		qs = self.filter_available(date_from, date_to, guests).order_by('date', 'time')

		event_ids = []
		filtered = []
		for run in qs:
			if not run.event.id in event_ids:
				filtered.append(run)
				event_ids.append(run.event.id)

		reverse, fields = (sort_by.startswith('-'), sort_by.lstrip('-').split('__'))

		criterion = lambda obj: get_related_attr(obj, fields)

		result = sorted(filtered, key=criterion, reverse=reverse)
		return result


class EventRunManager(models.Manager):

	def get_queryset(self):
		return EventRunQuerySet(self.model, using=self._db)

class EventRunManager(models.Manager):

	def get_queryset(self):
		return EventRunQuerySet(self.model, using=self._db)


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
	slug = models.SlugField(max_length=200, unique=True, null=True)
	created = models.DateTimeField(auto_now_add=True, null=True)
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
		unique_together = (("name", "host"),)

	def active_runs(self):
		today = timezone.now().date()
		return self.eventrun_set.filter(date__gte=today)

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name + '-with-' + self.host.username)
		super().save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('events:detail', args=[self.slug])


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

	objects = EventRunManager()


	def __str__(self):
		return '{}|{} ({})'.format(self.date, self.event, self.event.category)

	class Meta:
		ordering = ['date', 'time']
