# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(unique=True, max_length=64),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='team',
            name='slug',
            field=models.SlugField(unique=True, max_length=128),
            preserve_default=True,
        ),
    ]
