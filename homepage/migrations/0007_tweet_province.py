# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0006_auto_20150226_0908'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='province',
            field=models.CharField(default='', max_length=50),
            preserve_default=True,
        ),
    ]
