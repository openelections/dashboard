# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Agency'
        db.create_table('agencies_agency', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=75)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('gov_level', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=75, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=75, blank=True)),
            ('state', self.gf('django.contrib.localflavor.us.models.USStateField')(max_length=2)),
            ('fec_page', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('agencies', ['Agency'])

        # Adding model 'PortalLink'
        db.create_table('agencies_portallink', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('agency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['agencies.Agency'])),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('live_or_cert', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('descrip', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
        ))
        db.send_create_signal('agencies', ['PortalLink'])

        # Adding model 'DataFormat'
        db.create_table('agencies_dataformat', (
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('agencies', ['DataFormat'])

        # Adding model 'ResultLink'
        db.create_table('agencies_resultlink', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('agency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['agencies.Agency'])),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('live_or_cert', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('descrip', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
        ))
        db.send_create_signal('agencies', ['ResultLink'])

        # Adding M2M table for field formats on 'ResultLink'
        db.create_table('agencies_resultlink_formats', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('resultlink', models.ForeignKey(orm['agencies.resultlink'], null=False)),
            ('dataformat', models.ForeignKey(orm['agencies.dataformat'], null=False))
        ))
        db.create_unique('agencies_resultlink_formats', ['resultlink_id', 'dataformat_id'])


    def backwards(self, orm):
        # Deleting model 'Agency'
        db.delete_table('agencies_agency')

        # Deleting model 'PortalLink'
        db.delete_table('agencies_portallink')

        # Deleting model 'DataFormat'
        db.delete_table('agencies_dataformat')

        # Deleting model 'ResultLink'
        db.delete_table('agencies_resultlink')

        # Removing M2M table for field formats on 'ResultLink'
        db.delete_table('agencies_resultlink_formats')


    models = {
        'agencies.agency': {
            'Meta': {'object_name': 'Agency'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '75', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'fec_page': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'gov_level': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'state': ('django.contrib.localflavor.us.models.USStateField', [], {'max_length': '2'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '75', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'agencies.dataformat': {
            'Meta': {'object_name': 'DataFormat'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'primary_key': 'True'})
        },
        'agencies.portallink': {
            'Meta': {'object_name': 'PortalLink'},
            'agency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['agencies.Agency']"}),
            'descrip': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'live_or_cert': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'agencies.resultlink': {
            'Meta': {'object_name': 'ResultLink'},
            'agency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['agencies.Agency']"}),
            'descrip': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'formats': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'resultformats'", 'symmetrical': 'False', 'to': "orm['agencies.DataFormat']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'live_or_cert': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['agencies']