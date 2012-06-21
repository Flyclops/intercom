# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AccessLogEntry'
        db.create_table('intercom_accesslogentry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(related_name='access_log', to=orm['intercom.Member'])),
            ('access_datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('intercom', ['AccessLogEntry'])


    def backwards(self, orm):
        # Deleting model 'AccessLogEntry'
        db.delete_table('intercom_accesslogentry')


    models = {
        'intercom.accesslogentry': {
            'Meta': {'object_name': 'AccessLogEntry'},
            'access_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'access_log'", 'to': "orm['intercom.Member']"})
        },
        'intercom.member': {
            'Meta': {'object_name': 'Member'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'default': "'852257'", 'unique': 'True', 'max_length': '32'}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_access': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'membership': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['intercom.MembershipType']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'tone': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'intercom.membershiptype': {
            'Meta': {'object_name': 'MembershipType'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '32', 'primary_key': 'True'})
        },
        'intercom.timerule': {
            'Meta': {'ordering': "('priority',)", 'object_name': 'TimeRule'},
            'closing_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'day': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_open': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'membership': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rules'", 'to': "orm['intercom.MembershipType']"}),
            'opening_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'priority': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['intercom']