# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Constant'
        db.create_table('constants_constant', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('savings_interest_rate', self.gf('django.db.models.fields.DecimalField')(max_digits=4, decimal_places=2)),
            ('loan_interest_rate', self.gf('django.db.models.fields.DecimalField')(max_digits=4, decimal_places=2)),
        ))
        db.send_create_signal('constants', ['Constant'])


    def backwards(self, orm):
        # Deleting model 'Constant'
        db.delete_table('constants_constant')


    models = {
        'constants.constant': {
            'Meta': {'object_name': 'Constant'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loan_interest_rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '4', 'decimal_places': '2'}),
            'savings_interest_rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '4', 'decimal_places': '2'})
        }
    }

    complete_apps = ['constants']