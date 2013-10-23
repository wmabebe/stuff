# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Create_Dividend'
        db.delete_table('balance_and_dividend_create_dividend')

        # Adding model 'Dividends_Account'
        db.create_table('balance_and_dividend_dividends_account', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dividend_id', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['members.Member'])),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=2)),
            ('last_amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=20, decimal_places=2)),
            ('creation_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 8, 13, 0, 0))),
            ('is_withdrawn', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_seen', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('seen_date', self.gf('django.db.models.fields.DateField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal('balance_and_dividend', ['Dividends_Account'])

        # Deleting field 'Dividend.last_amount'
        db.delete_column('balance_and_dividend_dividend', 'last_amount')

        # Deleting field 'Dividend.member'
        db.delete_column('balance_and_dividend_dividend', 'member_id')

        # Deleting field 'Dividend.seen_date'
        db.delete_column('balance_and_dividend_dividend', 'seen_date')

        # Deleting field 'Dividend.is_withdrawn'
        db.delete_column('balance_and_dividend_dividend', 'is_withdrawn')

        # Deleting field 'Dividend.dividend_id'
        db.delete_column('balance_and_dividend_dividend', 'dividend_id')

        # Deleting field 'Dividend.is_seen'
        db.delete_column('balance_and_dividend_dividend', 'is_seen')

        # Adding field 'Dividend.total_savings'
        db.add_column('balance_and_dividend_dividend', 'total_savings',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=20, decimal_places=2),
                      keep_default=False)

        # Adding field 'Dividend.is_applied'
        db.add_column('balance_and_dividend_dividend', 'is_applied',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'Create_Dividend'
        db.create_table('balance_and_dividend_create_dividend', (
            ('is_applied', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('creation_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 8, 10, 0, 0))),
            ('amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=20, decimal_places=2)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('total_savings', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=20, decimal_places=2)),
        ))
        db.send_create_signal('balance_and_dividend', ['Create_Dividend'])

        # Deleting model 'Dividends_Account'
        db.delete_table('balance_and_dividend_dividends_account')

        # Adding field 'Dividend.last_amount'
        db.add_column('balance_and_dividend_dividend', 'last_amount',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=20, decimal_places=2),
                      keep_default=False)

        # Adding field 'Dividend.member'
        db.add_column('balance_and_dividend_dividend', 'member',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['members.Member']),
                      keep_default=False)

        # Adding field 'Dividend.seen_date'
        db.add_column('balance_and_dividend_dividend', 'seen_date',
                      self.gf('django.db.models.fields.DateField')(default=None, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Dividend.is_withdrawn'
        db.add_column('balance_and_dividend_dividend', 'is_withdrawn',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Dividend.dividend_id'
        db.add_column('balance_and_dividend_dividend', 'dividend_id',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=10),
                      keep_default=False)

        # Adding field 'Dividend.is_seen'
        db.add_column('balance_and_dividend_dividend', 'is_seen',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Deleting field 'Dividend.total_savings'
        db.delete_column('balance_and_dividend_dividend', 'total_savings')

        # Deleting field 'Dividend.is_applied'
        db.delete_column('balance_and_dividend_dividend', 'is_applied')


    models = {
        'balance_and_dividend.dividend': {
            'Meta': {'object_name': 'Dividend'},
            'amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '20', 'decimal_places': '2'}),
            'creation_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 8, 13, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_applied': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'total_savings': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '20', 'decimal_places': '2'})
        },
        'balance_and_dividend.dividends_account': {
            'Meta': {'object_name': 'Dividends_Account'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '2'}),
            'creation_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 8, 13, 0, 0)'}),
            'dividend_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_seen': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_withdrawn': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '20', 'decimal_places': '2'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['members.Member']"}),
            'seen_date': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        'balance_and_dividend.savings_account': {
            'Meta': {'object_name': 'Savings_Account'},
            'account_id': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'balance': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '20', 'decimal_places': '2'}),
            'creation_date': ('django.db.models.fields.DateField', [], {}),
            'deposit': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '20', 'decimal_places': '2'}),
            'guaranteed': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '20', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interest': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '20', 'decimal_places': '2'}),
            'interest_rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '4', 'decimal_places': '2'}),
            'is_seen': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_deposit': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(1970, 1, 1, 0, 0)'}),
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
            'member_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'office_phone_number': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'registration_date': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'salary': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'savings_percentage': ('django.db.models.fields.DecimalField', [], {'max_digits': '4', 'decimal_places': '2'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'subcity': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'university_id': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'wereda': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['balance_and_dividend']