# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import bitfield.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, db_index=True)),
                ('url', models.URLField(null=True, blank=True)),
                ('is_active', models.BooleanField(default=True, db_index=True)),
                ('language', models.CharField(max_length=2)),
                ('game_time', models.CharField(default=b'100: before start', max_length=200, null=True, blank=True)),
            ],
            options={
                'db_table': 'webapp_poissonmagique_campaign',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('mail_address', models.EmailField(max_length=75, db_index=True)),
                ('campaign', models.ForeignKey(to='poissonmagique.Campaign')),
            ],
            options={
                'db_table': 'webapp_poissonmagique_character',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Fragment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('when', models.DateTimeField()),
                ('game_time', models.CharField(default=b'', max_length=200, null=True, blank=True)),
            ],
            options={
                'db_table': 'webapp_poissonmagique_fragment',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FragmentRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rel_type', models.CharField(max_length=3, choices=[(b'FWD', b'Forward'), (b'RPL', b'Reply'), (b'REL', b'Related')])),
            ],
            options={
                'db_table': 'webapp_poissonmagique_fragmentrelation',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Human',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('mail_address', models.EmailField(unique=True, max_length=75, db_index=True)),
                ('is_bouncing', models.BooleanField(default=False)),
                ('campaign', models.ForeignKey(blank=True, to='poissonmagique.Campaign', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'db_table': 'webapp_poissonmagique_human',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('fragment_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='poissonmagique.Fragment')),
                ('message_id', models.CharField(unique=True, max_length=255, db_index=True)),
                ('subject', models.CharField(default=b'', max_length=255, null=True, blank=True)),
                ('status', bitfield.models.BitField(((b'read', b'Read'), (b'deleted', b'Deleted'), (b'private', b'Private')), default=0)),
                ('parts', models.ManyToManyField(related_name=b'part', to='poissonmagique.Fragment', blank=True)),
                ('receivers_character', models.ManyToManyField(related_name=b'receiver_character', to='poissonmagique.Character', blank=True)),
                ('receivers_human', models.ManyToManyField(related_name=b'receiver_human', to='poissonmagique.Human')),
            ],
            options={
                'db_table': 'webapp_poissonmagique_message',
            },
            bases=('poissonmagique.fragment',),
        ),
        migrations.CreateModel(
            name='MessageID',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message_id', models.CharField(max_length=255, db_index=True)),
                ('key', models.CharField(max_length=255, db_index=True)),
            ],
            options={
                'db_table': 'webapp_poissonmagique_messageid',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Queue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, db_index=True)),
                ('maildir', models.CharField(unique=True, max_length=1024, db_index=True)),
            ],
            options={
                'db_table': 'webapp_poissonmagique_queue',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('state_key', models.CharField(max_length=512)),
                ('from_address', models.EmailField(max_length=75)),
                ('state', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'webapp_poissonmagique_userstate',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='messageid',
            name='queue',
            field=models.ForeignKey(to='poissonmagique.Queue'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='messageid',
            unique_together=set([('message_id', 'key', 'queue')]),
        ),
        migrations.AddField(
            model_name='fragmentrelation',
            name='source',
            field=models.ForeignKey(related_name=b'source', to='poissonmagique.Fragment'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fragmentrelation',
            name='target',
            field=models.ForeignKey(related_name=b'target', to='poissonmagique.Fragment'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fragment',
            name='author_character',
            field=models.ForeignKey(blank=True, to='poissonmagique.Character', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fragment',
            name='author_human',
            field=models.ForeignKey(to='poissonmagique.Human'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fragment',
            name='campaign',
            field=models.ForeignKey(to='poissonmagique.Campaign'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='character',
            name='controller',
            field=models.ForeignKey(to='poissonmagique.Human'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='campaign',
            name='gm',
            field=models.ForeignKey(related_name=b'gm', to='poissonmagique.Human'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='campaign',
            name='players',
            field=models.ManyToManyField(default=None, related_name=b'players', to='poissonmagique.Human'),
            preserve_default=True,
        ),
    ]
