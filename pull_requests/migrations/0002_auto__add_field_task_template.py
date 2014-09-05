# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Task.template'
        db.add_column(u'pull_requests_task', 'template',
                      self.gf('django.db.models.fields.CharField')(default='None', max_length=255),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Task.template'
        db.delete_column(u'pull_requests_task', 'template')


    models = {
        u'pull_requests.pr': {
            'Meta': {'object_name': 'PR'},
            'current_commit_head': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'pull_requests.run': {
            'Meta': {'object_name': 'Run'},
            'datestamp': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pr': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pr'", 'to': u"orm['pull_requests.PR']"}),
            'result': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'pull_requests.task': {
            'Meta': {'object_name': 'Task'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'output': ('django.db.models.fields.TextField', [], {}),
            'result': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'run': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'run'", 'to': u"orm['pull_requests.Run']"}),
            'template': ('django.db.models.fields.CharField', [], {'default': "'None'", 'max_length': '255'})
        }
    }

    complete_apps = ['pull_requests']
