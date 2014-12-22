# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserCourse'
        db.create_table(u'interaction_usercourse', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['courses.Course'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('withdrawn', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('completed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('history', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'interaction', ['UserCourse'])

        # Adding unique constraint on 'UserCourse', fields ['course', 'user']
        db.create_unique(u'interaction_usercourse', ['course_id', 'user_id'])

        # Adding model 'UserLesson'
        db.create_table(u'interaction_userlesson', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lesson', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lesson.Lesson'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('visited', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('completed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('history', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'interaction', ['UserLesson'])

        # Adding unique constraint on 'UserLesson', fields ['lesson', 'user']
        db.create_unique(u'interaction_userlesson', ['lesson_id', 'user_id'])

        # Adding model 'UserLearningIntention'
        db.create_table(u'interaction_userlearningintention', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('learning_intention', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['outcome.LearningIntention'])),
        ))
        db.send_create_signal(u'interaction', ['UserLearningIntention'])

        # Adding unique constraint on 'UserLearningIntention', fields ['user', 'learning_intention']
        db.create_unique(u'interaction_userlearningintention', ['user_id', 'learning_intention_id'])

        # Adding model 'UserLearningIntentionDetail'
        db.create_table(u'interaction_userlearningintentiondetail', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('learning_intention_detail', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['outcome.LearningIntentionDetail'])),
            ('condition', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('history', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'interaction', ['UserLearningIntentionDetail'])

        # Adding unique constraint on 'UserLearningIntentionDetail', fields ['user', 'learning_intention_detail']
        db.create_unique(u'interaction_userlearningintentiondetail', ['user_id', 'learning_intention_detail_id'])

        # Adding model 'UserAttachment'
        db.create_table(u'interaction_userattachment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('attachment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['attachment.Attachment'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('history', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'interaction', ['UserAttachment'])

        # Adding unique constraint on 'UserAttachment', fields ['attachment', 'user']
        db.create_unique(u'interaction_userattachment', ['attachment_id', 'user_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'UserAttachment', fields ['attachment', 'user']
        db.delete_unique(u'interaction_userattachment', ['attachment_id', 'user_id'])

        # Removing unique constraint on 'UserLearningIntentionDetail', fields ['user', 'learning_intention_detail']
        db.delete_unique(u'interaction_userlearningintentiondetail', ['user_id', 'learning_intention_detail_id'])

        # Removing unique constraint on 'UserLearningIntention', fields ['user', 'learning_intention']
        db.delete_unique(u'interaction_userlearningintention', ['user_id', 'learning_intention_id'])

        # Removing unique constraint on 'UserLesson', fields ['lesson', 'user']
        db.delete_unique(u'interaction_userlesson', ['lesson_id', 'user_id'])

        # Removing unique constraint on 'UserCourse', fields ['course', 'user']
        db.delete_unique(u'interaction_usercourse', ['course_id', 'user_id'])

        # Deleting model 'UserCourse'
        db.delete_table(u'interaction_usercourse')

        # Deleting model 'UserLesson'
        db.delete_table(u'interaction_userlesson')

        # Deleting model 'UserLearningIntention'
        db.delete_table(u'interaction_userlearningintention')

        # Deleting model 'UserLearningIntentionDetail'
        db.delete_table(u'interaction_userlearningintentiondetail')

        # Deleting model 'UserAttachment'
        db.delete_table(u'interaction_userattachment')


    models = {
        u'attachment.attachment': {
            'Meta': {'unique_together': "(('lesson', 'seq'), ('course', 'seq'))", 'object_name': 'Attachment'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['courses.Course']", 'null': 'True', 'blank': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lesson.Lesson']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'seq': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
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
        u'interaction.userattachment': {
            'Meta': {'unique_together': "(('attachment', 'user'),)", 'object_name': 'UserAttachment'},
            'attachment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['attachment.Attachment']"}),
            'history': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'interaction.usercourse': {
            'Meta': {'unique_together': "(('course', 'user'),)", 'object_name': 'UserCourse'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['courses.Course']"}),
            'history': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'withdrawn': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'interaction.userlearningintention': {
            'Meta': {'unique_together': "(('user', 'learning_intention'),)", 'object_name': 'UserLearningIntention'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'learning_intention': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['outcome.LearningIntention']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'interaction.userlearningintentiondetail': {
            'Meta': {'unique_together': "(('user', 'learning_intention_detail'),)", 'object_name': 'UserLearningIntentionDetail'},
            'condition': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'history': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'learning_intention_detail': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['outcome.LearningIntentionDetail']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'interaction.userlesson': {
            'Meta': {'unique_together': "(('lesson', 'user'),)", 'object_name': 'UserLesson'},
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'history': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lesson.Lesson']"}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'visited': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'lesson.lesson': {
            'Meta': {'object_name': 'Lesson'},
            'abstract': ('django.db.models.fields.TextField', [], {}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['courses.Course']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'outcome.learningintention': {
            'Meta': {'object_name': 'LearningIntention'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lesson.Lesson']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'outcome.learningintentiondetail': {
            'Meta': {'object_name': 'LearningIntentionDetail'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'learning_intention': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['outcome.LearningIntention']"}),
            'lid_type': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['interaction']