# Generated by Django 2.1.2 on 2019-04-08 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_auto_20190323_1849'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventrun',
            options={'ordering': ['date', 'time']},
        ),
        migrations.AlterField(
            model_name='event',
            name='slug',
            field=models.SlugField(max_length=200, null=True, unique=True),
        ),
    ]
