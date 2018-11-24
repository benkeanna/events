from django.forms import ModelForm

from .models import Event


class CreateEventForm(ModelForm):
    """
    Event creation form.
    """
    class Meta:
        model = Event
        fields = [
            'name',
            'description',
            'location',
            'category',
        ]
