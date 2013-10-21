# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserState'
        db.create_table(u'poissonmagique_userstate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('state_key', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('from_address', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'poissonmagique', ['UserState'])

        # Adding model 'Human'
        db.create_table(u'poissonmagique_human', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('mail_address', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75, db_index=True)),
            ('campaign', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['poissonmagique.Campaign'], null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('is_bouncing', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'poissonmagique', ['Human'])

        # Adding model 'Campaign'
        db.create_table(u'poissonmagique_campaign', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, db_index=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('gm', self.gf('django.db.models.fields.related.ForeignKey')(related_name='gm', to=orm['poissonmagique.Human'])),
            ('players', self.gf('django.db.models.fields.related.ForeignKey')(related_name='player', to=orm['poissonmagique.Human'])),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True, db_index=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal(u'poissonmagique', ['Campaign'])

        # Adding model 'Character'
        db.create_table(u'poissonmagique_character', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('controller', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['poissonmagique.Human'])),
            ('campaign', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['poissonmagique.Campaign'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('mail_address', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75, db_index=True)),
        ))
        db.send_create_signal(u'poissonmagique', ['Character'])

        # Adding model 'Fragment'
        db.create_table(u'poissonmagique_fragment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sender', unique=True, to=orm['poissonmagique.Character'])),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('when', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'poissonmagique', ['Fragment'])

        # Adding M2M table for field related on 'Fragment'
        m2m_table_name = db.shorten_name(u'poissonmagique_fragment_related')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_fragment', models.ForeignKey(orm[u'poissonmagique.fragment'], null=False)),
            ('to_fragment', models.ForeignKey(orm[u'poissonmagique.fragment'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_fragment_id', 'to_fragment_id'])

        # Adding model 'Message'
        db.create_table(u'poissonmagique_message', (
            (u'fragment_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['poissonmagique.Fragment'], unique=True, primary_key=True)),
            ('receivers', self.gf('django.db.models.fields.related.ForeignKey')(related_name='receiver', to=orm['poissonmagique.Character'])),
        ))
        db.send_create_signal(u'poissonmagique', ['Message'])

        # Adding M2M table for field parts on 'Message'
        m2m_table_name = db.shorten_name(u'poissonmagique_message_parts')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('message', models.ForeignKey(orm[u'poissonmagique.message'], null=False)),
            ('fragment', models.ForeignKey(orm[u'poissonmagique.fragment'], null=False))
        ))
        db.create_unique(m2m_table_name, ['message_id', 'fragment_id'])


    def backwards(self, orm):
        # Deleting model 'UserState'
        db.delete_table(u'poissonmagique_userstate')

        # Deleting model 'Human'
        db.delete_table(u'poissonmagique_human')

        # Deleting model 'Campaign'
        db.delete_table(u'poissonmagique_campaign')

        # Deleting model 'Character'
        db.delete_table(u'poissonmagique_character')

        # Deleting model 'Fragment'
        db.delete_table(u'poissonmagique_fragment')

        # Removing M2M table for field related on 'Fragment'
        db.delete_table(db.shorten_name(u'poissonmagique_fragment_related'))

        # Deleting model 'Message'
        db.delete_table(u'poissonmagique_message')

        # Removing M2M table for field parts on 'Message'
        db.delete_table(db.shorten_name(u'poissonmagique_message_parts'))


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
        u'poissonmagique.campaign': {
            'Meta': {'object_name': 'Campaign'},
            'gm': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'gm'", 'to': u"orm['poissonmagique.Human']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'players': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'player'", 'to': u"orm['poissonmagique.Human']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'poissonmagique.character': {
            'Meta': {'object_name': 'Character'},
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['poissonmagique.Campaign']"}),
            'controller': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['poissonmagique.Human']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mail_address': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'poissonmagique.fragment': {
            'Meta': {'object_name': 'Fragment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sender'", 'unique': 'True', 'to': u"orm['poissonmagique.Character']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'related': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'related_rel_+'", 'to': u"orm['poissonmagique.Fragment']"}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'when': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'poissonmagique.human': {
            'Meta': {'object_name': 'Human'},
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['poissonmagique.Campaign']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_bouncing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mail_address': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'})
        },
        u'poissonmagique.message': {
            'Meta': {'object_name': 'Message', '_ormbases': [u'poissonmagique.Fragment']},
            u'fragment_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['poissonmagique.Fragment']", 'unique': 'True', 'primary_key': 'True'}),
            'parts': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'part'", 'symmetrical': 'False', 'to': u"orm['poissonmagique.Fragment']"}),
            'receivers': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'receiver'", 'to': u"orm['poissonmagique.Character']"})
        },
        u'poissonmagique.userstate': {
            'Meta': {'object_name': 'UserState'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'from_address': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'state_key': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        }
    }

    complete_apps = ['poissonmagique']