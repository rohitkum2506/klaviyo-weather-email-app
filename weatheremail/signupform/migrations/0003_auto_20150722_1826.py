# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('signupform', '0002_auto_20150722_1815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weathersubscription',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
