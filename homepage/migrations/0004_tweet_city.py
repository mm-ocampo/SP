# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0003_tweetlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='city',
            field=models.CharField(max_length=50, default=''),
            preserve_default=True,
        ),
    ]
