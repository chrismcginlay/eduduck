# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LearningIntention',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=200)),
                ('lesson', models.ForeignKey(help_text=b'parent lesson for this intention', to='lesson.Lesson')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LearningIntentionDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=200)),
                ('lid_type', models.CharField(max_length=2, choices=[('SC', b'Success Criterion'), ('LO', b'Learning Outcome')])),
                ('learning_intention', models.ForeignKey(help_text=b'parent learning intention for this criterion', to='outcome.LearningIntention')),
            ],
            options={
                'verbose_name': 'learning intention detail',
            },
            bases=(models.Model,),
        ),
    ]
