# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('poissonmagique', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Roll',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('when', models.DateTimeField()),
                ('game_time', models.CharField(default=b'', max_length=200, null=True, blank=True)),
                ('description', models.CharField(default=b'', max_length=400, null=True, blank=True)),
                ('what', models.CharField(default=b'', max_length=1024, null=True, blank=True)),
                ('hashid', models.PositiveIntegerField(unique=True, db_index=True)),
                ('implementation_type', models.IntegerField(default=1)),
                ('implementation_key', models.IntegerField()),
                ('campaign', models.ForeignKey(to='poissonmagique.Campaign')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RollOutcome',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('outcome_text', models.TextField()),
                ('roll', models.ForeignKey(to='dice.Roll')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SecureDice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('query_str', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='roll',
            name='outcome',
            field=models.ForeignKey(related_name=b'outcome', default=None, blank=True, to='dice.RollOutcome', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='roll',
            name='target',
            field=models.ForeignKey(blank=True, to='poissonmagique.Human', null=True),
            preserve_default=True,
        ),
    ]
