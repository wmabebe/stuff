# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing M2M table for field guarantors on 'Loan_Disbursement'
        db.delete_table('loan_loan_disbursement_guarantors')

        # Adding field 'Guarantee.loan'
        db.add_column('loan_guarantee', 'loan',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['loan.Loan_Request']),
                      keep_default=False)

        # Removing M2M table for field guarantors on 'Loan_Request'
        db.delete_table('loan_loan_request_guarantors')


    def backwards(self, orm):
        # Adding M2M table for field guarantors on 'Loan_Disbursement'
        db.create_table('loan_loan_disbursement_guarantors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('loan_disbursement', models.ForeignKey(orm['loan.loan_disbursement'], null=False)),
            ('guarantee', models.ForeignKey(orm['loan.guarantee'], null=False))
        ))
        db.create_unique('loan_loan_disbursement_guarantors', ['loan_disbursement_id', 'guarantee_id'])

        # Deleting field 'Guarantee.loan'
        db.delete_column('loan_guarantee', 'loan_id')

        # Adding M2M table for field guarantors on 'Loan_Request'
        db.create_table('loan_loan_request_guarantors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('loan_request', models.ForeignKey(orm['loan.loan_request'], null=False)),
            ('guarantee', models.ForeignKey(orm['loan.guarantee'], null=False))
        ))
        db.create_unique('loan_loan_request_guarantors', ['loan_request_id', 'guarantee_id'])


    models = {
        'loan.guarantee': {
            'Meta': {'object_name': 'Guarantee'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'guarantor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'guarantor'", 'null': 'True', 'to': "orm['members.Member']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_seen': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'loan': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['loan.Loan_Request']"}),
            'percentage': ('django.db.models.fields.DecimalField', [], {'max_digits': '4', 'decimal_places': '2'}),
            'seen_date': ('django.db.models.fields.DateField', [], {})
        },
        'loan.loan_disbursement': {
            'Meta': {'object_name': 'Loan_Disbursement'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'disbursement_date': ('django.db.models.fields.DateField', [], {}),
            'guaranteed': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interest': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'interest_rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '4', 'decimal_places': '2'}),
            'is_activated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_extended': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_renewed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_seen': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_settled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_payment': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(1970, 1, 1, 0, 0)'}),
            'loan_request': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['loan.Loan_Request']"}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['members.Member']"}),
            'principal': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'remaining': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'repayment_date': ('django.db.models.fields.DateField', [], {}),
            'repayment_rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'seen_date': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        'loan.loan_extension': {
            'Meta': {'object_name': 'Loan_Extension'},
            'current_repayment_date': ('django.db.models.fields.DateField', [], {}),
            'extension_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_seen': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'loan': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['loan.Loan_Disbursement']"}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['members.Member']"}),
            'previous_repayment_date': ('django.db.models.fields.DateField', [], {}),
            'seen_date': ('django.db.models.fields.DateField', [], {})
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
            'guaranteed': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interest': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'is_accepted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_seen': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_terminated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['members.Member']"}),
            'principal': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'request_date': ('django.db.models.fields.DateField', [], {}),
            'request_reason': ('django.db.models.fields.TextField', [], {}),
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