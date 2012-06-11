# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TimeRule'
        db.create_table('intercom_timerule', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('day', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('is_open', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('opening_time', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('closing_time', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('membership', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rules', to=orm['intercom.MembershipType'])),
        ))
        db.send_create_signal('intercom', ['TimeRule'])


    def backwards(self, orm):
        # Deleting model 'TimeRule'
        db.delete_table('intercom_timerule')


    models = {
        'intercom.member': {
            'Meta': {'object_name': 'Member'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'default': "'905895'", 'unique': 'True', 'max_length': '32'}),
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
            'Meta': {'object_name': 'TimeRule'},
            'closing_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'day': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_open': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'membership': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rules'", 'to': "orm['intercom.MembershipType']"}),
            'opening_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['intercom']