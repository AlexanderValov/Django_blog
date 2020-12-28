# Generated by Django 3.1.4 on 2020-12-28 15:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0009_auto_20201228_1804'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='moderators',
            field=models.ManyToManyField(blank=True, related_name='moderators', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='readers',
            field=models.ManyToManyField(blank=True, related_name='readers', to=settings.AUTH_USER_MODEL),
        ),
    ]