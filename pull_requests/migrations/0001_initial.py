# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PR'
        db.create_table(u'pull_requests_pr', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('current_commit_head', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'pull_requests', ['PR'])

        # Adding model 'Run'
        db.create_table(u'pull_requests_run', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pr', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pr', to=orm['pull_requests.PR'])),
            ('result', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('datestamp', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'pull_requests', ['Run'])

        # Adding model 'Task'
        db.create_table(u'pull_requests_task', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('run', self.gf('django.db.models.fields.related.ForeignKey')(related_name='run', to=orm['pull_requests.Run'])),
            ('output', self.gf('django.db.models.fields.TextField')()),
            ('result', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'pull_requests', ['Task'])


    def backwards(self, orm):
        # Deleting model 'PR'
        db.delete_table(u'pull_requests_pr')

        # Deleting model 'Run'
        db.delete_table(u'pull_requests_run')

        # Deleting model 'Task'
        db.delete_table(u'pull_requests_task')


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
            'run': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'run'", 'to': u"orm['pull_requests.Run']"})
        }
    }

    complete_apps = ['pull_requests']
