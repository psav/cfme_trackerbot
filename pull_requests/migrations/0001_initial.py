# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PR'
        db.create_table(u'pull_requests_pr', (
            ('number', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('current_commit_head', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('wip', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'pull_requests', ['PR'])

        # Adding model 'Run'
        db.create_table(u'pull_requests_run', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pr', self.gf('django.db.models.fields.related.ForeignKey')(related_name='run_set', to=orm['pull_requests.PR'])),
            ('commit', self.gf('django.db.models.fields.CharField')(default='None', max_length=255)),
            ('datestamp', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'pull_requests', ['Run'])

        # Adding model 'Task'
        db.create_table(u'pull_requests_task', (
            ('tid', self.gf('django.db.models.fields.CharField')(max_length=16, primary_key=True)),
            ('run', self.gf('django.db.models.fields.related.ForeignKey')(related_name='task_set', null=True, to=orm['pull_requests.Run'])),
            ('datestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('output', self.gf('django.db.models.fields.TextField')()),
            ('result', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('stream', self.gf('django.db.models.fields.CharField')(default='None', max_length=255)),
            ('template', self.gf('django.db.models.fields.CharField')(default='None', max_length=255)),
            ('provider', self.gf('django.db.models.fields.CharField')(default='None', max_length=255)),
            ('vm_name', self.gf('django.db.models.fields.CharField')(default='None', max_length=255)),
            ('cleanup', self.gf('django.db.models.fields.BooleanField')(default=False)),
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
            'number': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'wip': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'pull_requests.run': {
            'Meta': {'object_name': 'Run'},
            'commit': ('django.db.models.fields.CharField', [], {'default': "'None'", 'max_length': '255'}),
            'datestamp': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pr': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'run_set'", 'to': u"orm['pull_requests.PR']"})
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