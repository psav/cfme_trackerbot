# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Template'
        db.create_table(u'provider_templates_template', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, primary_key=True)),
            ('datestamp', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='templates', to=orm['provider_templates.Group'])),
        ))
        db.send_create_signal(u'provider_templates', ['Template'])

        # Adding model 'Provider'
        db.create_table(u'provider_templates_provider', (
            ('key', self.gf('django.db.models.fields.CharField')(max_length=255, primary_key=True)),
        ))
        db.send_create_signal(u'provider_templates', ['Provider'])

        # Adding model 'ProviderTemplateDetail'
        db.create_table(u'provider_templates_providertemplatedetail', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(related_name='providertemplatedetail', to=orm['provider_templates.Template'])),
            ('provider', self.gf('django.db.models.fields.related.ForeignKey')(related_name='providertemplatedetail', to=orm['provider_templates.Provider'])),
            ('usable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tested', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('concat_id', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'provider_templates', ['ProviderTemplateDetail'])

        # Adding unique constraint on 'ProviderTemplateDetail', fields ['template', 'provider']
        db.create_unique(u'provider_templates_providertemplatedetail', ['template_id', 'provider_id'])

        # Adding model 'Group'
        db.create_table(u'provider_templates_group', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=63, primary_key=True)),
        ))
        db.send_create_signal(u'provider_templates', ['Group'])


    def backwards(self, orm):
        # Removing unique constraint on 'ProviderTemplateDetail', fields ['template', 'provider']
        db.delete_unique(u'provider_templates_providertemplatedetail', ['template_id', 'provider_id'])

        # Deleting model 'Template'
        db.delete_table(u'provider_templates_template')

        # Deleting model 'Provider'
        db.delete_table(u'provider_templates_provider')

        # Deleting model 'ProviderTemplateDetail'
        db.delete_table(u'provider_templates_providertemplatedetail')

        # Deleting model 'Group'
        db.delete_table(u'provider_templates_group')


    models = {
        u'provider_templates.group': {
            'Meta': {'ordering': "['name']", 'object_name': 'Group'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '63', 'primary_key': 'True'})
        },
        u'provider_templates.provider': {
            'Meta': {'ordering': "['key']", 'object_name': 'Provider'},
            'key': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'})
        },
        u'provider_templates.providertemplatedetail': {
            'Meta': {'ordering': "['concat_id']", 'unique_together': "(('template', 'provider'),)", 'object_name': 'ProviderTemplateDetail'},
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