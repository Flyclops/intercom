# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        MembershipType = orm['intercom.MembershipType']

        for mt in MembershipType.objects.all():
            priority = 0
            for rule in mt.rules.all():
                rule.priority = priority
                rule.save()
                priority += 1

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        'intercom.member': {
            'Meta': {'object_name': 'Member'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'default': "'786073'", 'unique': 'True', 'max_length': '32'}),
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
    symmetrical = True
