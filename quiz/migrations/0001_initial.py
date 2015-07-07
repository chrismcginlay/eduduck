# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer_text', models.TextField(verbose_name=b'possible answer')),
                ('explan_text', models.TextField(help_text=b'Advice on how relevant this answer is', verbose_name=b'answer advice')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question_text', models.TextField(help_text=b'The question as presented to the user')),
                ('answers', models.ManyToManyField(to='quiz.Answer', verbose_name=b'possible answers')),
                ('correct_answer', models.ForeignKey(related_name=b'valid', to='quiz.Answer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuestionAttempt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField(default=0)),
                ('answer_given', models.ForeignKey(verbose_name=b"user's answer", to='quiz.Answer')),
                ('question', models.ForeignKey(to='quiz.Question')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quiz_title', models.CharField(max_length=200)),
                ('create_date', models.DateField(auto_now=True, verbose_name=b'date quiz created')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('lesson', models.ForeignKey(to='lesson.Lesson')),
                ('questions', models.ManyToManyField(to='quiz.Question')),
            ],
            options={
                'verbose_name': 'quiz',
                'verbose_name_plural': 'quizzes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuizAttempt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('taken_dt', models.DateTimeField(verbose_name=b'date of quiz attempt')),
                ('quiz', models.ForeignKey(to='quiz.Quiz')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='questionattempt',
            name='quiz_attempt',
            field=models.ForeignKey(to='quiz.QuizAttempt'),
            preserve_default=True,
        ),
    ]
