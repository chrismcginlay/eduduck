# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name=b'lesson title')),
                ('abstract', models.TextField(help_text=b'summary of the lesson in a couple of paragraphs')),
                ('course', models.ForeignKey(help_text=b'course to which this lesson belongs', to='courses.Course')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
