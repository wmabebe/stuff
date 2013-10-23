# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Savings_Account'
        db.create_table('balance_and_dividend_savings_account', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account_id', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['members.Member'])),
            ('balance', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('savings_percentage', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('interest_rate', self.gf('django.db.models.fields.DecimalField')(max_digits=4, decimal_places=2)),
            ('creation_date', self.gf('django.db.models.fields.DateField')()),
            ('is_seen', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('seen_date', self.gf('django.db.models.fields.DateField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal('balance_and_dividend', ['Savings_Account'])

        # Adding model 'Dividend'
        db.create_table('balance_and_dividend_dividend', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dividend_id', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['members.Member'])),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('creation_date', self.gf('django.db.models.fields.DateField')()),
            ('is_seen', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('seen_date', self.gf('django.db.models.fields.DateField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal('balance_and_dividend', ['Dividend'])


    def backwards(self, orm):
        # Deleting model 'Savings_Account'
        db.delete_table('balance_and_dividend_savings_account')

        # Deleting model 'Dividend'
        db.delete_table('balance_and_dividend_dividend')


    models = {
        'balance_and_dividend.dividend': {
            'Meta': {'object_name': 'Dividend'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'creation_date': ('django.db.models.fields.DateField', [], {}),
            'dividend_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_seen': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['members.Member']"}),
            'seen_date': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        'balance_and_dividend.savings_account': {
            'Meta': {'object_name': 'Savings_Account'},
            'account_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'balance': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'creation_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interest_rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '4', 'decimal_places': '2'}),
            'is_seen': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['members.Member']"}),
            'savings_percentage': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'seen_date': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
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
        }
    }

    complete_apps = ['balance_and_dividend']