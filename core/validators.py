import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_human_name(value):

	regex = r'^[A-Za-z\s\-]+$'
	if not re.match(regex, value):
		raise ValidationError(
			_('Names can contain only alpha characters'),
			code='invalid')
