# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Group.active'
        db.add_column(u'provider_templates_group', 'active',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Group.active'
        db.delete_column(u'provider_templates_group', 'active')


    models = {
        u'provider_templates.group': {
            'Meta': {'ordering': "['name']", 'object_name': 'Group'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '63', 'primary_key': 'True'}),
            'stream': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'provider_templates.provider': {
            'Meta': {'ordering': "['key']", 'object_name': 'Provider'},
            'key': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'})
        },
        u'provider_templates.providertemplatedetail': {
            'Meta': {'ordering': "['-template__datestamp', 'concat_id']", 'unique_together': "(('template', 'provider'),)", 'object_name': 'ProviderTemplateDetail'},
            'concat_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'providertemplatedetail'", 'to': u"orm['provider_templates.Provider']"}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'providertemplatedetail'", 'to': u"orm['provider_templates.Template']"}),
            'tested': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'usable': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'provider_templates.template': {
            'Meta': {'ordering': "['-datestamp']", 'object_name': 'Template'},
            'datestamp': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'templates'", 'to': u"orm['provider_templates.Group']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'providers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'templates'", 'symmetrical': 'False', 'through': u"orm['provider_templates.ProviderTemplateDetail']", 'to': u"orm['provider_templates.Provider']"})
        }
    }

    complete_apps = ['provider_templates']
