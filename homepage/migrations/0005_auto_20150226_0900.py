# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0004_tweet_city'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='keyword',
            name='id',
        ),
        migrations.AlterField(
            model_name='keyword',
            name='word',
            field=models.CharField(primary_key=True, max_length=128, serialize=False),
            preserve_default=True,
        ),
    ]
