# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0001_initial'),
        ('outcome', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('attachment', '0001_initial'),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAttachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('history', models.TextField(null=True, blank=True)),
                ('attachment', models.ForeignKey(help_text=b'attachment user is downloading', to='attachment.Attachment')),
                ('user', models.ForeignKey(help_text=b'User interacting with attachment', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserCourse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True)),
                ('withdrawn', models.BooleanField(default=False)),
                ('completed', models.BooleanField(default=False)),
                ('history', models.TextField(null=True, blank=True)),
                ('course', models.ForeignKey(help_text=b'Course user is referring to', to='courses.Course')),
                ('user', models.ForeignKey(help_text=b'User interacting with course', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserLearningIntention',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('learning_intention', models.ForeignKey(help_text=b'Learning intention user is interacting with', to='outcome.LearningIntention')),
                ('user', models.ForeignKey(help_text=b'User interacting with LI', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserLearningIntentionDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('condition', models.SmallIntegerField(default=0)),
                ('history', models.TextField(null=True, blank=True)),
                ('learning_intention_detail', models.ForeignKey(help_text=b'Success criterion or learning outcome user is interacting with', to='outcome.LearningIntentionDetail')),
                ('user', models.ForeignKey(help_text=b'User interacting with LI detail', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': "user's learning intention detail",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserLesson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('visited', models.BooleanField(default=False)),
                ('completed', models.BooleanField(default=False)),
                ('history', models.TextField(null=True, blank=True)),
                ('note', models.TextField(null=True, blank=True)),
                ('lesson', models.ForeignKey(help_text=b'Lesson user is interacting with', to='lesson.Lesson')),
                ('user', models.ForeignKey(help_text=b'User interacting with course', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='userlesson',
            unique_together=set([('lesson', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='userlearningintentiondetail',
            unique_together=set([('user', 'learning_intention_detail')]),
        ),
        migrations.AlterUniqueTogether(
            name='userlearningintention',
            unique_together=set([('user', 'learning_intention')]),
        ),
        migrations.AlterUniqueTogether(
            name='usercourse',
            unique_together=set([('course', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='userattachment',
            unique_together=set([('attachment', 'user')]),
        ),
    ]
