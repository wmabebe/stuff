# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Loan_Disbursement.last_payment_date_date'
        db.delete_column('loan_loan_disbursement', 'last_payment_date_date')

        # Adding field 'Loan_Disbursement.last_payment_date'
        db.add_column('loan_loan_disbursement', 'last_payment_date',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(1970, 1, 1, 0, 0)),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Loan_Disbursement.last_payment_date_date'
        db.add_column('loan_loan_disbursement', 'last_payment_date_date',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(1970, 1, 1, 0, 0)),
                      keep_default=False)

        # Deleting field 'Loan_Disbursement.last_payment_date'
        db.delete_column('loan_loan_disbursement', 'last_payment_date')


    models = {
        'loan.guarantee': {
            'Meta': {'object_name': 'Guarantee'},
            'amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'}),
            'applied_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'}),
            'created_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 8, 10, 0, 0)'}),
            'guarantor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'guarantor'", 'null': 'True', 'to': "orm['members.Member']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_applied': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_seen': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'loan_request': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['loan.Loan_Request']"}),
            'percentage': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '2'}),
            'seen_date': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        'loan.loan_disbursement': {
            'Meta': {'object_name': 'Loan_Disbursement'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'disbursement_date': ('django.db.models.fields.DateField', [], {}),
            'guaranteed': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interest': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'interest_rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '4', 'decimal_places': '2'}),
            'is_activated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_extended': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_guaranteed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_renewed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_seen': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_settled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_payment_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'}),
            'last_payment_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(1970, 1, 1, 0, 0)'}),
            'loan_request': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['loan.Loan_Request']"}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['members.Member']"}),
            'principal': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'remaining': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'}),
            'repayment_date': ('django.db.models.fields.DateField', [], {}),
            'repayment_rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'seen_date': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        'loan.loan_extension': {
            'Meta': {'object_name': 'Loan_Extension'},
            'current_repayment_date': ('django.db.models.fields.DateField', [], {}),
            'extension_date': ('django.db.models.fields.DateField', [], {}),
            'extension_months': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_seen': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'loan': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['loan.Loan_Disbursement']"}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['members.Member']"}),
            'previous_repayment_date': ('django.db.models.fields.DateField', [], {}),
            'seen_date': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        'loan.loan_renewal': {
            'Meta': {'object_name': 'Loan_Renewal'},
            'current_loan_amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'current_repayment_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_seen': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'loan': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['loan.Loan_Disbursement']"}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['members.Member']"}),
            'previous_loan_amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'previous_repayment_date': ('django.db.models.fields.DateField', [], {}),
            'renewal_amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'renewal_date': ('django.db.models.fields.DateField', [], {}),
            'seen_date': ('django.db.models.fields.DateField', [], {})
        },
        'loan.loan_request': {
            'Meta': {'object_name': 'Loan_Request'},
            'accountant_approval': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'cashier_grant': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'comments': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'cp_vcp_approval': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'current_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'}),
            'guaranteed': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interest': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'is_accepted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_guaranteed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_seen': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_terminated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['members.Member']"}),
            'principal': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'request_date': ('django.db.models.fields.DateField', [], {}),
            'request_reason': ('django.db.models.fields.TextField', [], {}),
            'required_adjustment': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'}),
            'required_guarantee_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'}),
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

    complete_apps = ['loan']