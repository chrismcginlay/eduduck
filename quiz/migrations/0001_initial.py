# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Answer'
        db.create_table(u'quiz_answer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('answer_text', self.gf('django.db.models.fields.TextField')()),
            ('explan_text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'quiz', ['Answer'])

        # Adding model 'Question'
        db.create_table(u'quiz_question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question_text', self.gf('django.db.models.fields.TextField')()),
            ('correct_answer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='valid', to=orm['quiz.Answer'])),
        ))
        db.send_create_signal(u'quiz', ['Question'])

        # Adding M2M table for field answers on 'Question'
        m2m_table_name = db.shorten_name(u'quiz_question_answers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('question', models.ForeignKey(orm[u'quiz.question'], null=False)),
            ('answer', models.ForeignKey(orm[u'quiz.answer'], null=False))
        ))
        db.create_unique(m2m_table_name, ['question_id', 'answer_id'])

        # Adding model 'Quiz'
        db.create_table(u'quiz_quiz', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('quiz_title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('lesson', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lesson.Lesson'])),
            ('create_date', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'quiz', ['Quiz'])

        # Adding M2M table for field questions on 'Quiz'
        m2m_table_name = db.shorten_name(u'quiz_quiz_questions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('quiz', models.ForeignKey(orm[u'quiz.quiz'], null=False)),
            ('question', models.ForeignKey(orm[u'quiz.question'], null=False))
        ))
        db.create_unique(m2m_table_name, ['quiz_id', 'question_id'])

        # Adding model 'QuizAttempt'
        db.create_table(u'quiz_quizattempt', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('quiz', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quiz.Quiz'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('taken_dt', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'quiz', ['QuizAttempt'])

        # Adding model 'QuestionAttempt'
        db.create_table(u'quiz_questionattempt', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('quiz_attempt', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quiz.QuizAttempt'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quiz.Question'])),
            ('answer_given', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quiz.Answer'])),
            ('score', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'quiz', ['QuestionAttempt'])


    def backwards(self, orm):
        # Deleting model 'Answer'
        db.delete_table(u'quiz_answer')

        # Deleting model 'Question'
        db.delete_table(u'quiz_question')

        # Removing M2M table for field answers on 'Question'
        db.delete_table(db.shorten_name(u'quiz_question_answers'))

        # Deleting model 'Quiz'
        db.delete_table(u'quiz_quiz')

        # Removing M2M table for field questions on 'Quiz'
        db.delete_table(db.shorten_name(u'quiz_quiz_questions'))

        # Deleting model 'QuizAttempt'
        db.delete_table(u'quiz_quizattempt')

        # Deleting model 'QuestionAttempt'
        db.delete_table(u'quiz_questionattempt')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'courses.course': {
            'Meta': {'object_name': 'Course'},
            'abstract': ('django.db.models.fields.TextField', [], {}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'courses_instructed_set'", 'to': u"orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'organiser': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'courses_organised_set'", 'to': u"orm['auth.User']"})
        },
        u'lesson.lesson': {
            'Meta': {'object_name': 'Lesson'},
            'abstract': ('django.db.models.fields.TextField', [], {}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['courses.Course']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'quiz.answer': {
            'Meta': {'object_name': 'Answer'},
            'answer_text': ('django.db.models.fields.TextField', [], {}),
            'explan_text': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'quiz.question': {
            'Meta': {'object_name': 'Question'},
            'answers': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['quiz.Answer']", 'symmetrical': 'False'}),
            'correct_answer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'valid'", 'to': u"orm['quiz.Answer']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question_text': ('django.db.models.fields.TextField', [], {})
        },
        u'quiz.questionattempt': {
            'Meta': {'object_name': 'QuestionAttempt'},
            'answer_given': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quiz.Answer']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quiz.Question']"}),
            'quiz_attempt': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quiz.QuizAttempt']"}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'quiz.quiz': {
            'Meta': {'object_name': 'Quiz'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'create_date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lesson.Lesson']"}),
            'questions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['quiz.Question']", 'symmetrical': 'False'}),
            'quiz_title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'quiz.quizattempt': {
            'Meta': {'object_name': 'QuizAttempt'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quiz': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quiz.Quiz']"}),
            'taken_dt': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['quiz']