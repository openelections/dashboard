# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Office'
        db.create_table('hub_office', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, primary_key=True)),
        ))
        db.send_create_signal('hub', ['Office'])

        # Adding model 'Organization'
        db.create_table('hub_organization', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=150)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('gov_agency', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('gov_level', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=75, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=75, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=2, db_index=True)),
            ('fec_page', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('hub', ['Organization'])

        # Adding model 'Contact'
        db.create_table('hub_contact', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('org', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hub.Organization'])),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('middle_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=70, blank=True)),
            ('phone', self.gf('django.contrib.localflavor.us.models.PhoneNumberField')(max_length=20, blank=True)),
            ('mobile', self.gf('django.contrib.localflavor.us.models.PhoneNumberField')(max_length=20, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=254, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('hub', ['Contact'])

        # Adding model 'DataFormat'
        db.create_table('hub_dataformat', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, primary_key=True)),
        ))
        db.send_create_signal('hub', ['DataFormat'])

        # Adding model 'State'
        db.create_table('hub_state', (
            ('postal', self.gf('django.db.models.fields.CharField')(max_length=2, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('hub', ['State'])

        # Adding model 'ElecData'
        db.create_table('hub_elecdata', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('race_type', self.gf('django.db.models.fields.CharField')(max_length=10, db_index=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')(db_index=True)),
            ('end_date', self.gf('django.db.models.fields.DateField')(db_index=True)),
            ('runoff_for', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('special', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('unexpired_term', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hub.State'])),
            ('office', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hub.Office'], null=True, blank=True)),
            ('district', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hub.Organization'], null=True)),
            ('portal_link', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('direct_link', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('result_type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('state_level', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('county_level', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('precinct_level', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('prez', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('senate', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('house', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('gov', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('state_officers', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('state_leg', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('local', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('hub', ['ElecData'])

        # Adding unique constraint on 'ElecData', fields ['race_type', 'end_date', 'special', 'unexpired_term', 'office', 'state', 'district']
        db.create_unique('hub_elecdata', ['race_type', 'end_date', 'special', 'unexpired_term', 'office_id', 'state_id', 'district'])

        # Adding M2M table for field formats on 'ElecData'
        db.create_table('hub_elecdata_formats', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('elecdata', models.ForeignKey(orm['hub.elecdata'], null=False)),
            ('dataformat', models.ForeignKey(orm['hub.dataformat'], null=False))
        ))
        db.create_unique('hub_elecdata_formats', ['elecdata_id', 'dataformat_id'])

        # Adding model 'Log'
        db.create_table('hub_log', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hub.State'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('org', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hub.Organization'], null=True, blank=True)),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hub.Contact'], null=True, blank=True)),
            ('formal_request', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('gdoc_link', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('follow_up', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('hub', ['Log'])


    def backwards(self, orm):
        # Removing unique constraint on 'ElecData', fields ['race_type', 'end_date', 'special', 'unexpired_term', 'office', 'state', 'district']
        db.delete_unique('hub_elecdata', ['race_type', 'end_date', 'special', 'unexpired_term', 'office_id', 'state_id', 'district'])

        # Deleting model 'Office'
        db.delete_table('hub_office')

        # Deleting model 'Organization'
        db.delete_table('hub_organization')

        # Deleting model 'Contact'
        db.delete_table('hub_contact')

        # Deleting model 'DataFormat'
        db.delete_table('hub_dataformat')

        # Deleting model 'State'
        db.delete_table('hub_state')

        # Deleting model 'ElecData'
        db.delete_table('hub_elecdata')

        # Removing M2M table for field formats on 'ElecData'
        db.delete_table('hub_elecdata_formats')

        # Deleting model 'Log'
        db.delete_table('hub_log')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
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
            'unexpired_term': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
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
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
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