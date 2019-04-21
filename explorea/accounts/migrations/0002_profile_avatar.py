# Generated by Django 2.1.2 on 2019-04-20 10:43

from django.db import migrations, models
import explorea.accounts.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(null=True, upload_to=explorea.accounts.models.image_dir, verbose_name='Upload your photo'),
        ),
    ]
