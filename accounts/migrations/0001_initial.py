# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, blank=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('email', models.EmailField(primary_key=True, max_length=254, serialize=False)),
                ('groups', models.ManyToManyField(blank=True, related_query_name='user', related_name='user_set', to='auth.Group', verbose_name='groups', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.')),
                ('user_permissions', models.ManyToManyField(blank=True, related_query_name='user', related_name='user_set', to='auth.Permission', verbose_name='user permissions', help_text='Specific permissions for this user.')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
