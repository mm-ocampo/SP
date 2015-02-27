# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0005_auto_20150226_0900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='keyword',
            field=models.ForeignKey(to='homepage.Keyword'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tweetlog',
            name='keyword',
            field=models.ForeignKey(to='homepage.Keyword'),
            preserve_default=True,
        ),
    ]
