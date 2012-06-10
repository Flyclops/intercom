# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MembershipType'
        db.create_table('intercom_membershiptype', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=32, primary_key=True)),
        ))
        db.send_create_signal('intercom', ['MembershipType'])

        # Adding model 'Member'
        db.create_table('intercom_member', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('membership', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['intercom.MembershipType'])),
            ('code', self.gf('django.db.models.fields.CharField')(default='466359', unique=True, max_length=32)),
            ('tone', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('last_access', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal('intercom', ['Member'])


    def backwards(self, orm):
        # Deleting model 'MembershipType'
        db.delete_table('intercom_membershiptype')

        # Deleting model 'Member'
        db.delete_table('intercom_member')


    models = {
        'intercom.member': {
            'Meta': {'object_name': 'Member'},
            'code': ('django.db.models.fields.CharField', [], {'default': "'959835'", 'unique': 'True', 'max_length': '32'}),
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
        }
    }

    complete_apps = ['intercom']