# Generated by Django 4.2.9 on 2024-01-14 13:18

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='members',
            field=models.ManyToManyField(blank=True, null=True, related_name='members_of_community', to=settings.AUTH_USER_MODEL),
        ),
    ]
