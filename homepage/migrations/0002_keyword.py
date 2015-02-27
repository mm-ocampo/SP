# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('word', models.CharField(max_length=128)),
                ('date', models.DateTimeField()),
                ('searchFrequency', models.PositiveSmallIntegerField(default=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
