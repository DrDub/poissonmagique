# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'RollBackend'
        db.delete_table(u'dice_rollbackend')

        # Deleting field 'Roll.implementation'
        db.delete_column(u'dice_roll', 'implementation_id')

        # Adding field 'Roll.implementation_type'
        db.add_column(u'dice_roll', 'implementation_type',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Adding field 'Roll.implementation_key'
        db.add_column(u'dice_roll', 'implementation_key',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Deleting field 'SecureDice.rollbackend_ptr'
        db.delete_column(u'dice_securedice', u'rollbackend_ptr_id')

        # Adding field 'SecureDice.id'
        db.add_column(u'dice_securedice', u'id',
                      self.gf('django.db.models.fields.AutoField')(primary_key=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'RollBackend'
        db.create_table(u'dice_rollbackend', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'dice', ['RollBackend'])

        # Adding field 'Roll.implementation'
        db.add_column(u'dice_roll', 'implementation',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['dice.RollBackend']),
                      keep_default=False)

        # Deleting field 'Roll.implementation_type'
        db.delete_column(u'dice_roll', 'implementation_type')

        # Deleting field 'Roll.implementation_key'
        db.delete_column(u'dice_roll', 'implementation_key')

        # Adding field 'SecureDice.rollbackend_ptr'
        db.add_column(u'dice_securedice', u'rollbackend_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=1, to=orm['dice.RollBackend'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'SecureDice.id'
        db.delete_column(u'dice_securedice', u'id')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'dice.roll': {
            'Meta': {'object_name': 'Roll'},
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['poissonmagique.Campaign']"}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'game_time': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'hashid': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'implementation_key': ('django.db.models.fields.IntegerField', [], {}),
            'implementation_type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'outcome': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'outcome'", 'null': 'True', 'blank': 'True', 'to': u"orm['dice.RollOutcome']"}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['poissonmagique.Human']", 'null': 'True', 'blank': 'True'}),
            'what': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'when': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'dice.rolloutcome': {
            'Meta': {'object_name': 'RollOutcome'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'outcome_text': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'roll': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dice.Roll']"})
        },
        u'dice.securedice': {
            'Meta': {'object_name': 'SecureDice'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'query_str': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'poissonmagique.campaign': {
            'Meta': {'object_name': 'Campaign'},
            'game_time': ('django.db.models.fields.CharField', [], {'default': "'100: before start'", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'gm': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'gm'", 'to': u"orm['poissonmagique.Human']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'players': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'related_name': "'players'", 'symmetrical': 'False', 'to': u"orm['poissonmagique.Human']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'poissonmagique.human': {
            'Meta': {'object_name': 'Human'},
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['poissonmagique.Campaign']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_bouncing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mail_address': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'})
        }
    }

    complete_apps = ['dice']
