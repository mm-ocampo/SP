# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0007_tweet_province'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='region',
            field=models.CharField(default='', max_length=70),
            preserve_default=True,
        ),
    ]
