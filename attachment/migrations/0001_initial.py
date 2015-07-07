# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0001_initial'),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('desc', models.TextField(null=True, blank=True)),
                ('seq', models.IntegerField(null=True, blank=True)),
                ('attachment', models.FileField(upload_to=b'attachments')),
                ('course', models.ForeignKey(blank=True, to='courses.Course', null=True)),
                ('lesson', models.ForeignKey(blank=True, to='lesson.Lesson', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='attachment',
            unique_together=set([('lesson', 'seq'), ('course', 'seq')]),
        ),
    ]
