# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Member'
        db.create_table('members_member', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('member_id', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('father_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('grand_father_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('subcity', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('wereda', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('house_number', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('house_phone_number', self.gf('django.db.models.fields.CharField')(max_length=13, null=True, blank=True)),
            ('office_phone_number', self.gf('django.db.models.fields.CharField')(max_length=13)),
            ('cell_phone_number', self.gf('django.db.models.fields.CharField')(max_length=13, null=True, blank=True)),
            ('POBox', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('birth_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('sex', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('campus', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('faculty', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('department', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('salary', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('employment_type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=200, null=True, blank=True)),
            ('application_date', self.gf('django.db.models.fields.DateField')()),
            ('is_registered', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('registration_date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('members', ['Member'])

        # Adding model 'Notification'
        db.create_table('members_notification', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('to', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['members.Member'])),
            ('sent_date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('members', ['Notification'])


    def backwards(self, orm):
        # Deleting model 'Member'
        db.delete_table('members_member')

        # Deleting model 'Notification'
        db.delete_table('members_notification')


    models = {
        'members.member': {
            'Meta': {'object_name': 'Member'},
            'POBox': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'application_date': ('django.db.models.fields.DateField', [], {}),
            'birth_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'campus': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'cell_phone_number': ('django.db.models.fields.CharField', [], {'max_length': '13', 'null': 'True', 'blank': 'True'}),
            'department': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'employment_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'faculty': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'father_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'grand_father_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'house_number': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'house_phone_number': ('django.db.models.fields.CharField', [], {'max_length': '13', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_registered': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'member_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'office_phone_number': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'registration_date': ('django.db.models.fields.DateField', [], {}),
            'salary': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'subcity': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'wereda': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'members.notification': {
            'Meta': {'object_name': 'Notification'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'sent_date': ('django.db.models.fields.DateField', [], {}),
            'to': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['members.Member']"})
        }
    }

    complete_apps = ['members']