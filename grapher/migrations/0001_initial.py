# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Build'
        db.create_table(u'grapher_build', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('stream', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['provider_templates.Group'])),
            ('datestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('passes', self.gf('django.db.models.fields.IntegerField')()),
            ('fails', self.gf('django.db.models.fields.IntegerField')()),
            ('skips', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'grapher', ['Build'])


    def backwards(self, orm):
        # Deleting model 'Build'
        db.delete_table(u'grapher_build')


    models = {
        u'grapher.build': {
            'Meta': {'object_name': 'Build'},
            'datestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'fails': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'passes': ('django.db.models.fields.IntegerField', [], {}),
            'skips': ('django.db.models.fields.IntegerField', [], {}),
            'stream': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['provider_templates.Group']"})
        },
        u'provider_templates.group': {
            'Meta': {'ordering': "['name']", 'object_name': 'Group'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '63', 'primary_key': 'True'}),
            'stream': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        }
    }

    complete_apps = ['grapher']