# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Run.retest'
        db.add_column(u'pull_requests_run', 'retest',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Run.retest'
        db.delete_column(u'pull_requests_run', 'retest')


    models = {
        u'pull_requests.pr': {
            'Meta': {'object_name': 'PR'},
            'current_commit_head': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'number': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'wip': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'pull_requests.run': {
            'Meta': {'object_name': 'Run'},
            'commit': ('django.db.models.fields.CharField', [], {'default': "'None'", 'max_length': '255'}),
            'datestamp': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pr': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'run_set'", 'to': u"orm['pull_requests.PR']"}),
            'retest': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'pull_requests.task': {
            'Meta': {'object_name': 'Task'},
            'cleanup': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'datestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'output': ('django.db.models.fields.TextField', [], {}),
            'provider': ('django.db.models.fields.CharField', [], {'default': "'None'", 'max_length': '255'}),
            'result': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'run': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'task_set'", 'null': 'True', 'to': u"orm['pull_requests.Run']"}),
            'stream': ('django.db.models.fields.CharField', [], {'default': "'None'", 'max_length': '255'}),
            'template': ('django.db.models.fields.CharField', [], {'default': "'None'", 'max_length': '255'}),
            'tid': ('django.db.models.fields.CharField', [], {'max_length': '16', 'primary_key': 'True'}),
            'vm_name': ('django.db.models.fields.CharField', [], {'default': "'None'", 'max_length': '255'})
        }
    }

    complete_apps = ['pull_requests']