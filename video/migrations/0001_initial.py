# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import video.utils


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0001_initial'),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('url', models.URLField(validators=[video.utils.validate_youtube_url])),
                ('course', models.ForeignKey(blank=True, to='courses.Course', null=True)),
                ('lesson', models.ForeignKey(blank=True, to='lesson.Lesson', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
