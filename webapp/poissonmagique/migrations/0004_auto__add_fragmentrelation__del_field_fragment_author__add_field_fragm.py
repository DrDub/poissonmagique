# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'MessageID', fields ['message_id']
        db.delete_unique(u'poissonmagique_messageid', ['message_id'])

        # Removing unique constraint on 'MessageID', fields ['key']
        db.delete_unique(u'poissonmagique_messageid', ['key'])

        # Removing unique constraint on 'Character', fields ['mail_address']
        db.delete_unique(u'poissonmagique_character', ['mail_address'])

        # Adding model 'FragmentRelation'
        db.create_table(u'poissonmagique_fragmentrelation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(related_name='source', to=orm['poissonmagique.Fragment'])),
            ('target', self.gf('django.db.models.fields.related.ForeignKey')(related_name='target', to=orm['poissonmagique.Fragment'])),
            ('rel_type', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal(u'poissonmagique', ['FragmentRelation'])

        # Deleting field 'Fragment.author'
        db.delete_column(u'poissonmagique_fragment', 'author_id')

        # Adding field 'Fragment.author_character'
        db.add_column(u'poissonmagique_fragment', 'author_character',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['poissonmagique.Character'], null=True),
                      keep_default=False)

        # Adding field 'Fragment.author_human'
        db.add_column(u'poissonmagique_fragment', 'author_human',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['poissonmagique.Human']),
                      keep_default=False)

        # Adding field 'Fragment.campaign'
        db.add_column(u'poissonmagique_fragment', 'campaign',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['poissonmagique.Campaign']),
                      keep_default=False)

        # Removing M2M table for field related on 'Fragment'
        db.delete_table(db.shorten_name(u'poissonmagique_fragment_related'))

        # Adding unique constraint on 'MessageID', fields ['message_id', 'key', 'queue']
        db.create_unique(u'poissonmagique_messageid', ['message_id', 'key', 'queue_id'])

        # Deleting field 'Message.receivers'
        db.delete_column(u'poissonmagique_message', 'receivers_id')

        # Adding field 'Message.status'
        db.add_column(u'poissonmagique_message', 'status',
                      self.gf('django.db.models.fields.BigIntegerField')(default=0),
                      keep_default=False)

        # Adding M2M table for field receivers_character on 'Message'
        m2m_table_name = db.shorten_name(u'poissonmagique_message_receivers_character')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('message', models.ForeignKey(orm[u'poissonmagique.message'], null=False)),
            ('character', models.ForeignKey(orm[u'poissonmagique.character'], null=False))
        ))
        db.create_unique(m2m_table_name, ['message_id', 'character_id'])

        # Adding M2M table for field receivers_human on 'Message'
        m2m_table_name = db.shorten_name(u'poissonmagique_message_receivers_human')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('message', models.ForeignKey(orm[u'poissonmagique.message'], null=False)),
            ('human', models.ForeignKey(orm[u'poissonmagique.human'], null=False))
        ))
        db.create_unique(m2m_table_name, ['message_id', 'human_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'MessageID', fields ['message_id', 'key', 'queue']
        db.delete_unique(u'poissonmagique_messageid', ['message_id', 'key', 'queue_id'])

        # Deleting model 'FragmentRelation'
        db.delete_table(u'poissonmagique_fragmentrelation')


        # User chose to not deal with backwards NULL issues for 'Fragment.author'
        raise RuntimeError("Cannot reverse this migration. 'Fragment.author' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Fragment.author'
        db.add_column(u'poissonmagique_fragment', 'author',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='sender', unique=True, to=orm['poissonmagique.Character']),
                      keep_default=False)

        # Deleting field 'Fragment.author_character'
        db.delete_column(u'poissonmagique_fragment', 'author_character_id')

        # Deleting field 'Fragment.author_human'
        db.delete_column(u'poissonmagique_fragment', 'author_human_id')

        # Deleting field 'Fragment.campaign'
        db.delete_column(u'poissonmagique_fragment', 'campaign_id')

        # Adding M2M table for field related on 'Fragment'
        m2m_table_name = db.shorten_name(u'poissonmagique_fragment_related')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_fragment', models.ForeignKey(orm[u'poissonmagique.fragment'], null=False)),
            ('to_fragment', models.ForeignKey(orm[u'poissonmagique.fragment'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_fragment_id', 'to_fragment_id'])

        # Adding unique constraint on 'Character', fields ['mail_address']
        db.create_unique(u'poissonmagique_character', ['mail_address'])

        # Adding unique constraint on 'MessageID', fields ['key']
        db.create_unique(u'poissonmagique_messageid', ['key'])

        # Adding unique constraint on 'MessageID', fields ['message_id']
        db.create_unique(u'poissonmagique_messageid', ['message_id'])


        # User chose to not deal with backwards NULL issues for 'Message.receivers'
        raise RuntimeError("Cannot reverse this migration. 'Message.receivers' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Message.receivers'
        db.add_column(u'poissonmagique_message', 'receivers',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='receiver', to=orm['poissonmagique.Character']),
                      keep_default=False)

        # Deleting field 'Message.status'
        db.delete_column(u'poissonmagique_message', 'status')

        # Removing M2M table for field receivers_character on 'Message'
        db.delete_table(db.shorten_name(u'poissonmagique_message_receivers_character'))

        # Removing M2M table for field receivers_human on 'Message'
        db.delete_table(db.shorten_name(u'poissonmagique_message_receivers_human'))


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
            'players': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'related_name': "'players'", 'symmetrical': 'False', 'to': u"orm['poissonmagique.Human']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'poissonmagique.character': {
            'Meta': {'object_name': 'Character'},
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['poissonmagique.Campaign']"}),
            'controller': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['poissonmagique.Human']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mail_address': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'poissonmagique.fragment': {
            'Meta': {'object_name': 'Fragment'},
            'author_character': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['poissonmagique.Character']", 'null': 'True'}),
            'author_human': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['poissonmagique.Human']"}),
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['poissonmagique.Campaign']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'when': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'poissonmagique.fragmentrelation': {
            'Meta': {'object_name': 'FragmentRelation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rel_type': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'source'", 'to': u"orm['poissonmagique.Fragment']"}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'target'", 'to': u"orm['poissonmagique.Fragment']"})
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
            'message_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'parts': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'part'", 'symmetrical': 'False', 'to': u"orm['poissonmagique.Fragment']"}),
            'receivers_character': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'receiver_character'", 'symmetrical': 'False', 'to': u"orm['poissonmagique.Character']"}),
            'receivers_human': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'receiver_human'", 'symmetrical': 'False', 'to': u"orm['poissonmagique.Human']"}),
            'status': ('django.db.models.fields.BigIntegerField', [], {'default': '0'})
        },
        u'poissonmagique.messageid': {
            'Meta': {'unique_together': "(('message_id', 'key', 'queue'),)", 'object_name': 'MessageID'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'message_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'queue': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['poissonmagique.Queue']"})
        },
        u'poissonmagique.queue': {
            'Meta': {'object_name': 'Queue'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maildir': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '1024', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
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