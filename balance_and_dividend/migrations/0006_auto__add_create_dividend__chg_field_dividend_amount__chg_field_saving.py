# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Create_Dividend'
        db.create_table('balance_and_dividend_create_dividend', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=20, decimal_places=2)),
            ('creation_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 8, 10, 0, 0))),
            ('total_savings', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=20, decimal_places=2)),
            ('is_applied', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('balance_and_dividend', ['Create_Dividend'])


        # Changing field 'Dividend.amount'
        db.alter_column('balance_and_dividend_dividend', 'amount', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=2))

        # Changing field 'Savings_Account.guaranteed'
        db.alter_column('balance_and_dividend_savings_account', 'guaranteed', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=2))

        # Changing field 'Savings_Account.deposit'
        db.alter_column('balance_and_dividend_savings_account', 'deposit', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=2))

        # Changing field 'Savings_Account.interest'
        db.alter_column('balance_and_dividend_savings_account', 'interest', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=2))

        # Changing field 'Savings_Account.balance'
        db.alter_column('balance_and_dividend_savings_account', 'balance', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=2))

    def backwards(self, orm):
        # Deleting model 'Create_Dividend'
        db.delete_table('balance_and_dividend_create_dividend')


        # Changing field 'Dividend.amount'
        db.alter_column('balance_and_dividend_dividend', 'amount', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2))

        # Changing field 'Savings_Account.guaranteed'
        db.alter_column('balance_and_dividend_savings_account', 'guaranteed', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2))

        # Changing field 'Savings_Account.deposit'
        db.alter_column('balance_and_dividend_savings_account', 'deposit', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2))

        # Changing field 'Savings_Account.interest'
        db.alter_column('balance_and_dividend_savings_account', 'interest', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2))

        # Changing field 'Savings_Account.balance'
        db.alter_column('balance_and_dividend_savings_account', 'balance', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2))

    models = {
        'balance_and_dividend.create_dividend': {
            'Meta': {'object_name': 'Create_Dividend'},
            'amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '20', 'decimal_places': '2'}),
            'creation_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 8, 10, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_applied': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'total_savings': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '20', 'decimal_places': '2'})
        },
        'balance_and_dividend.dividend': {
            'Meta': {'object_name': 'Dividend'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '2'}),
            'creation_date': ('django.db.models.fields.DateField', [], {}),
            'dividend_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_seen': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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