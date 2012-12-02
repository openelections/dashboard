# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Log.follow_up'
        db.alter_column('hub_log', 'follow_up', self.gf('django.db.models.fields.DateField')(null=True))

    def backwards(self, orm):

        # Changing field 'Log.follow_up'
        db.alter_column('hub_log', 'follow_up', self.gf('django.db.models.fields.DateField')(default=None))

    models = {
        'hub.contact': {
            'Meta': {'object_name': 'Contact'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'mobile': ('django.contrib.localflavor.us.models.PhoneNumberField', [], {'max_length': '20', 'blank': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'org': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hub.Organization']"}),
            'phone': ('django.contrib.localflavor.us.models.PhoneNumberField', [], {'max_length': '20', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '70', 'blank': 'True'})
        },
        'hub.dataformat': {
            'Meta': {'object_name': 'DataFormat'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'primary_key': 'True'})
        },
        'hub.elecdata': {
            'Meta': {'unique_together': "(('race_type', 'end_date', 'special', 'unexpired_term', 'office', 'state', 'district'),)", 'object_name': 'ElecData'},
            'county_level': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'direct_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'district': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            'formats': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['hub.DataFormat']", 'symmetrical': 'False'}),
            'gov': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'house': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'office': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hub.Office']", 'null': 'True', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hub.Organization']", 'null': 'True'}),
            'portal_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'precinct_level': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'prez': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'race_type': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_index': 'True'}),
            'result_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'runoff_for': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'senate': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'special': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hub.State']"}),
            'state_leg': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'state_level': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'state_officers': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'unexpired_term': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'})
        },
        'hub.log': {
            'Meta': {'object_name': 'Log'},
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hub.Contact']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'follow_up': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'formal_request': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'gdoc_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'org': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hub.Organization']", 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hub.State']"}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'hub.office': {
            'Meta': {'ordering': "['name']", 'object_name': 'Office'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'primary_key': 'True'})
        },
        'hub.organization': {
            'Meta': {'object_name': 'Organization'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '75', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'fec_page': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'gov_agency': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'gov_level': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '150'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2', 'db_index': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '75', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'hub.state': {
            'Meta': {'ordering': "['name']", 'object_name': 'State'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'postal': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True'})
        }
    }

    complete_apps = ['hub']