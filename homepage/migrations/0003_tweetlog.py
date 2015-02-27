# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0002_keyword'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tweetlog',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('keyword', models.CharField(max_length=128)),
                ('sinceId', models.CharField(max_length=50)),
                ('maxId', models.CharField(max_length=50)),
                ('date', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
