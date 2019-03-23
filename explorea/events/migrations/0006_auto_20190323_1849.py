from django.conf import settings
from django.db import migrations, models

from django.utils.text import slugify

def to_slug(apps, schema_editor):

    Event = apps.get_model('events', 'Event')
    for event in Event.objects.all():
        event.slug = slugify(event.name + '-with-' + event.host.username)
        event.save()

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0005_auto_20181209_1407'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['name']},
        ),
        migrations.AddField(
            model_name='event',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='slug',
            field=models.SlugField(max_length=200, null=True, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='event',
            unique_together={('name', 'host')},
        ),

        migrations.RunPython(to_slug),
        migrations.AlterField(
            model_name='event',
            name='slug',
            field=models.SlugField(null=False, max_length=200, unique=True),
        ),
    ]