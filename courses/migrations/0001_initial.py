# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(help_text=b"optional course code for author's reference", max_length=10, blank=True)),
                ('name', models.CharField(help_text=b'human readable short name of the course', max_length=20)),
                ('abstract', models.TextField(help_text=b'summary of the course in a couple of paragraphs')),
                ('instructor', models.ForeignKey(related_name=b'courses_instructed_set', to=settings.AUTH_USER_MODEL, help_text=b'This user is providing the instruction')),
                ('organiser', models.ForeignKey(related_name=b'courses_organised_set', to=settings.AUTH_USER_MODEL, help_text=b'This user is organising the course')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
